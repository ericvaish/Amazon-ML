import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
import numbers

# ----------------------------------------------------------
# Calculate Line Angle (x1,y1,x2,y2) -> Angle
# ----------------------------------------------------------
def calculate_line_angle(x1, y1, x2, y2):
    """Calculate angle of a line for Hough Transform."""
    angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
    print(f"Line from ({x1}, {y1}) to ({x2}, {y2}) has an angle of {angle:.2f} degrees.")
    return angle

# ----------------------------------------------------------
# Calculate Line Angle (x1,y1,x2,y2) -> Angle
# ----------------------------------------------------------
def classify_line(image, entity):
    # Classify lines as horizontal (width) or vertical (height).
    print(f"Classifying entities by line in the cropped region, entity check for: {entity}")
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=5)

        if lines is None:
            print(f"No lines detected in image.")
            return None
        
        print(f"Total lines detected: {len(lines)}")
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = calculate_line_angle(x1, y1, x2, y2)

            if entity == 'width':
                if -15 <= angle <= 15:
                    print(f"Horizontal line detected with angle: {angle}. Classified as width.")
                    return 'width'
            elif entity == 'height':
                if 75 <= abs(angle) <= 105:
                    print(f"Vertical line detected with angle: {angle}. Classified as height.")
                    return 'height'
        return None
    except Exception as e:
        print(f"Error in classify_line: {e}")
        return None


def extend_bounding_box(bbox, image_width, image_height, extend_px=50):
    # Extend bounding boxes by a certain size.
    print(f"Original bounding box: {bbox}")
    try:
        (tl, tr, br, bl) = bbox

        # Convert to NumPy arrays for manipulation.
        tl = np.array(tl) 
        tr = np.array(tr)
        br = np.array(br)
        bl = np.array(bl)

        # Adjust bounding box coordinates by extending.
        tl[0] = max(0, tl[0] - extend_px)
        tl[1] = max(0, tl[1] - extend_px)

        tr[0] = min(image_width - 1, tr[0] + extend_px)
        tr[1] = max(0, tr[1] - extend_px)

        br[0] = min(image_width - 1, br[0] + extend_px)
        br[1] = min(image_height - 1, br[1] + extend_px)

        bl[0] = max(0, bl[0] - extend_px)
        bl[1] = min(image_height - 1, bl[1] + extend_px)

        extended_bbox = [tuple(tl), tuple(tr), tuple(br), tuple(bl)]
        print(f"Extended bounding box: {extended_bbox}")
        return extended_bbox
    except Exception as e:
        print(f"Error extending bounding box: {e}")
        return bbox  # If an error occurs, return the original bounding box.


def contains_numbers(text):
    # Check if a string contains any digits.
    print(f"Checking if the text '{text}' contains numbers.")
    result = any(char.isdigit() for char in text)
    print(f"Text '{text}' contains numbers: {result}")
    return result

def draw_bounding_boxes(image, boxes, color=(0, 255, 0)):
    #Draw bounding boxes on the image.
    print(f"Drawing {len(boxes)} bounding boxes.")
    try:
        for box in boxes:
            box = np.array(box, dtype=np.int32)
            cv2.polylines(image, [box], isClosed=True, color=color, thickness=2)
        return image
    except Exception as e:
        print(f"Error in draw_bounding_boxes: {e}")
        return image

def display_image(image, title="Image"):
    """Display an image using matplotlib."""
    print(f"Displaying image with title: {title}")
    try:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Error in display_image: {e}")

def detect_entity_in_image(image_path, entity):
    if entity == 'depth':
        entity = 'width'
        
    print(f"\nStarting detection process for entity: {entity} \n")
    try:
        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'], gpu=True)  # gpu=False if you're not using GPU

        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image from path: {image_path}")
            return None
        # ----------------------------------------------------------
        # Step 1: Detect all texts and show original bounding boxes
        # ----------------------------------------------------------

        results = reader.readtext(image)

        # Debug: Check if results are empty
        if results:
            print(f"\nResults detected: {results}\n")
        else:
            print("No text found in the image.")
            return None, results
        
        # Number of boxes
        all_bboxes = [r[0] for r in results]
        print(f"Total number of text blocks detected: {len(all_bboxes)}")

        # Define length and height of image
        image_height, image_width = image.shape[:2]
        image_copy = image.copy()



        display_image(draw_bounding_boxes(image.copy(), all_bboxes), "All Bounding Boxes")

        # ----------------------------------------------------------
        # Step 2: Filter for number-containing text
        # ----------------------------------------------------------

        number_bboxes_text = [(r[0], r[1]) for r in results if contains_numbers(r[1])]
        number_bboxes = [bbox for bbox, text in number_bboxes_text]

        # 
        # text = text.replace(",", ".") if text else text

        print(f"Total number of number-containing text blocks: {len(number_bboxes)}")

        # Display only the bounding boxes which contain numbers
        display_image(draw_bounding_boxes(image.copy(), number_bboxes, color=(255, 0, 0)), "Bounding Boxes with Numbers")

        # ----------------------------------------------------------
        # Step 3: Extend bounding boxes by 50px
        # ----------------------------------------------------------

        extended_bboxes = [extend_bounding_box(bbox, image_width, image_height, extend_px=50) for bbox in number_bboxes]
        print(f"Extended bounding boxes: {extended_bboxes}")

        display_image(draw_bounding_boxes(image.copy(), extended_bboxes, color=(0, 0, 255)), "Extended Bounding Boxes by 50px")

    
        # ----------------------------------------------------------
        # Step 4: Process text regions and classify them
        # ----------------------------------------------------------

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Step 4.1: Iterate over the bounding boxes and CLASSIFY corresponding Extended Bounded Boxes as Width or Height.
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for bbox, (extended_bbox, text) in zip(number_bboxes, zip(extended_bboxes, [t[1] for t in number_bboxes_text])):
            text = text.replace(",", ".") if text else text
            print(f"\nProcessing text region for: '{text}'\n")
            
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Step 4.2: Extract ROI (Region of Interest) from the extended bounding box
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            try:
                x_min = int(min([point[0] for point in extended_bbox]))
                y_min = int(min([point[1] for point in extended_bbox]))
                x_max = int(max([point[0] for point in extended_bbox]))
                y_max = int(max([point[1] for point in extended_bbox]))

                roi = image[y_min:y_max, x_min:x_max]
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                # Step 4.3: IGNORING FOR NOW
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                # Step 4.4: Classify the extracted ROI based on the entity (width or height)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

                classification_result = classify_line(roi, entity)


                if classification_result == entity:
                    print(f"Match found: Detected {entity} for '{text}'")
                    result = text
                    found_entity = True

                    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    # Step 4.6: Annotate the image with the classification result
                    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

                    cv2.putText(image_copy, classification_result, (x_min, y_min - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                else:
                    print(f"Entity not matching for '{text}'. Classification result: {classification_result}")
            except Exception as e:
                print(f"Error processing ROI for text '{text}': {e}")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Step 4.7: Display the final image with annotations
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        display_image(image_copy, f"Final Classification: {entity.capitalize()}")

        if not found_entity:
            print(f"No '{entity}' found in the image.")
        else:
            print(f"Successfully detected '{entity}'!")
        

        return result



    except Exception as e:
        print(f"Error in detect_entity_in_image: {e}")
        return None


image_path = '/Users/ericvaish/Downloads/Amazon/Height_2500/41XM9J3d5SL.jpg'
entity = 'height'  # entity type: 'height' or 'width'

result = detect_entity_in_image(image_path, entity)

print("----------")
print(f"Detected entity: {result}")
print("----------")





import cv2
import numpy as np
import os

def preprocess_image(filepath, techniques=None):
    """
    Applies image preprocessing techniques based on user selection.
    Techniques: resizing, grayscale, noise_removal, equalization, edge_detection
    """
    if not os.path.exists(filepath):
        raise ValueError(f"File not found at: {filepath}")

    if techniques is None:
        techniques = ['resizing', 'grayscale', 'noise_removal', 'equalization', 'edge_detection']

    # Handle PDF conversion if necessary
    if filepath.lower().endswith('.pdf'):
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        page = doc.load_page(0)  # Load the first page
        pix = page.get_pixmap()
        img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        # Convert RGB to BGR for OpenCV
        if pix.n == 3: # RGB
            image = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
        elif pix.n == 4: # RGBA
            image = cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)
        else: # Gray
            image = img_data
    else:
        # Load the image normally
        image = cv2.imread(filepath)

    if image is None:
        file_size = os.path.getsize(filepath)
        raise ValueError(f"Invalid image format or corrupted file. Ext: {os.path.splitext(filepath)[1]}, Size: {file_size} bytes")

    # Always resize to standard dimensions first for consistency
    if 'resizing' in techniques:
        standard_size = (800, 1000)
        image = cv2.resize(image, standard_size)

    processed_data = {'original': image.copy()}
    curr_image = image

    # 1. Grayscale Conversion
    if 'grayscale' in techniques:
        curr_image = cv2.cvtColor(curr_image, cv2.COLOR_BGR2GRAY)
        processed_data['gray'] = curr_image.copy()

    # 2. Noise Removal (Gaussian Filter)
    if 'noise_removal' in techniques:
        # Check if 1-channel or 3-channel
        curr_image = cv2.GaussianBlur(curr_image, (5, 5), 0)
        processed_data['blurred'] = curr_image.copy()

    # 3. Histogram Equalization (Contrast enhancement)
    if 'equalization' in techniques:
        # Equalization requires grayscale
        if len(curr_image.shape) == 3:
            gray = cv2.cvtColor(curr_image, cv2.COLOR_BGR2GRAY)
            curr_image = cv2.equalizeHist(gray)
        else:
            curr_image = cv2.equalizeHist(curr_image)
        processed_data['equalized'] = curr_image.copy()

    # 4. Edge Detection (Canny)
    if 'edge_detection' in techniques:
        if len(curr_image.shape) == 3:
            gray = cv2.cvtColor(curr_image, cv2.COLOR_BGR2GRAY)
            curr_image = cv2.Canny(gray, 30, 100)
        else:
            curr_image = cv2.Canny(curr_image, 30, 100)
        processed_data['edges'] = curr_image.copy()

    # Final result for feature extraction
    processed_data['final'] = curr_image
    
    # Compatibility with feature extractor (needs 'gray' and 'original')
    if 'gray' not in processed_data:
        if len(image.shape) == 3:
            processed_data['gray'] = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            processed_data['gray'] = image

    return processed_data

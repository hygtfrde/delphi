import cv2
import numpy as np

class PageFlattener:
    def __init__(self, noise_threshold=5000):
        self.noise_threshold = noise_threshold

    def convert_to_grayscale(self, image):
        """
        Convert the image to grayscale.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def apply_gaussian_blur(self, image, kernel_size=(5, 5), sigma=0):
        """
        Apply Gaussian Blur to reduce noise.
        """
        return cv2.GaussianBlur(image, kernel_size, sigma)

    def detect_edges(self, image, low_threshold=50, high_threshold=150):
        """
        Detect edges using Canny edge detection.
        """
        return cv2.Canny(image, low_threshold, high_threshold)

    def find_largest_contour(self, edges):
        """
        Find the largest contour in the edge-detected image.
        """
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        if contours:
            return contours[0]
        else:
            return None

    def approximate_contour(self, contour, epsilon_factor=0.02):
        """
        Approximate the contour to a quadrilateral.
        """
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    def order_points(self, points):
        """
        Order points in a consistent manner for perspective transform.
        """
        rect = np.zeros((4, 2), dtype="float32")
        s = points.sum(axis=1)
        rect[0] = points[np.argmin(s)]
        rect[2] = points[np.argmax(s)]
        diff = np.diff(points, axis=1)
        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]
        return rect

    def compute_dimensions(self, points):
        """
        Compute the width and height of the transformed image.
        """
        (tl, tr, br, bl) = points
        width_a = np.linalg.norm(br - bl)
        width_b = np.linalg.norm(tr - tl)
        max_width = max(int(width_a), int(width_b))

        height_a = np.linalg.norm(tr - br)
        height_b = np.linalg.norm(tl - bl)
        max_height = max(int(height_a), int(height_b))

        return max_width, max_height

    def apply_perspective_transform(self, image, src_points, dst_size):
        """
        Apply a perspective transform to the image.
        """
        dst_points = np.array([
            [0, 0],
            [dst_size[0] - 1, 0],
            [dst_size[0] - 1, dst_size[1] - 1],
            [0, dst_size[1] - 1]], dtype="float32")

        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        return cv2.warpPerspective(image, matrix, dst_size)

    def flatten_and_fix_frames(self, image, show_steps=False):
        """
        Main method to flatten and fix curvy images of pages.
        """
        gray = self.convert_to_grayscale(image)
        if show_steps:
            cv2.imshow("Grayscale", gray)
            cv2.waitKey(0)

        blurred = self.apply_gaussian_blur(gray)
        if show_steps:
            cv2.imshow("Blurred", blurred)
            cv2.waitKey(0)

        edges = self.detect_edges(blurred)
        if show_steps:
            cv2.imshow("Edges", edges)
            cv2.waitKey(0)

        largest_contour = self.find_largest_contour(edges)
        if largest_contour is None:
            print("No contour found.")
            return image

        if show_steps:
            contour_image = image.copy()
            cv2.drawContours(contour_image, [largest_contour], -1, (0, 255, 0), 2)
            cv2.imshow("Page Contour", contour_image)
            cv2.waitKey(0)

        approx_contour = self.approximate_contour(largest_contour)
        if len(approx_contour) != 4:
            print("Could not find a four-point contour. The page might not be detected correctly.")
            return image

        ordered_points = self.order_points(approx_contour.reshape(4, 2))
        max_width, max_height = self.compute_dimensions(ordered_points)
        flattened_image = self.apply_perspective_transform(image, ordered_points, (max_width, max_height))

        if show_steps:
            cv2.imshow("Flattened Image", flattened_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return flattened_image

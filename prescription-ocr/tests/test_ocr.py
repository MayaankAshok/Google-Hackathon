import unittest
from src.ocr.processor import process_image

class TestOCRProcessing(unittest.TestCase):

    def test_process_image_valid(self):
        # Assuming 'valid_prescription_image.jpg' is a valid test image
        result = process_image('tests/valid_prescription_image.jpg')
        self.assertIsInstance(result, dict)
        self.assertIn('medicines', result)
        self.assertIn('details', result)

    def test_process_image_invalid(self):
        # Assuming 'invalid_image.txt' is an invalid test image
        result = process_image('tests/invalid_image.txt')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
from PIL import Image
import os

def test_conversion():
    # Create dummy image
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save('test_input.png')
    
    # Convert
    img = Image.open('test_input.png')
    img.save('test_output.webp', 'webp')
    
    # Check
    if os.path.exists('test_output.webp'):
        print("Conversion test PASSED: test_output.webp created.")
    else:
        print("Conversion test FAILED.")
        exit(1)

    # Cleanup
    try:
        os.remove('test_input.png')
        os.remove('test_output.webp')
    except:
        pass

if __name__ == "__main__":
    test_conversion()

# Finger Counter with OpenCV and Mediapipe

This project uses OpenCV and Mediapipe to detect hands and count the number of stretched fingers in a video. It also detects faces and blurs them for privacy.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- Matplotlib

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/finger-counter-open-cv.git
    cd finger-counter-open-cv
    ```

2. Install the required packages:
    ```sh
    pip install opencv-python mediapipe matplotlib
    ```

## Usage

1. Replace the `video_path` variable in `main.py` with the path to your video file:
    ```python
    video_path = 'path/to/your/video.mp4'
    ```

2. Run the script:
    ```sh
    python main.py
    ```

3. The video will be displayed in a window. Press 'q' to quit the video display.

## Features

- Detects hands and counts the number of stretched fingers.
- Detects faces and blurs them for privacy.
- Displays the processed video with annotations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/)
- [Mediapipe](https://mediapipe.dev/)

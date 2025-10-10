Made with Python, based on https://gist.github.com/robert/b0b14b1fd4a5feb2b45ab3ce049f5707

Install the required libraries with `pip install -r requirements.txt`

Usage: `./ascii.py [option]`

Options:

-f, --filename  : Filename of the video file you desire to be processed to ASCII, incompatible with the -wc/--webcam option. (string)

-wc, --webcam   : Live processing of video from webcam. (boolean: True | False)

-i, --invert    : Option for inverting the output. (boolean: True | False)

TODO:
- ~~Some form of concurrency?~~ This turned out to be an awful idea
- [ ] A pop of colour 
- [ ] Audio
- [x] Options for IO type
- [ ] Options for resolution?
- [ ] GUI
- [x] Live interpolation

## CREDITS

Made with Python, based on https://gist.github.com/robert/b0b14b1fd4a5feb2b45ab3ce049f5707

## REQUIREMENTS

Install the required libraries with `pip install -r requirements.txt`. Furthermore, > C++ Build tools 14 needed for cython compilation of functions library.

## USAGE
With these requirements complete, the application can be run with `./run.sh`.This will compile the functions library into a usable state. If you wish to build the libraries manually, you can by running `python setup.py build_ext --inplace`, then run the application with `ascii.py [-h] [-f FILENAME] [-wc WEBCAM] [--invert] [--colour]`.

## OPTIONS:

-f, --filename  : Filename of the video file you desire to be processed to ASCII, incompatible with the -wc/--webcam option. (string)

-wc, --webcam   : Live processing of video from webcam. (boolean: True | False)

--invert    : Option for inverting the output.

--colour        : Option for interpreting colour rather than the default green-black monochromatic interpretation.

## TODO:
- ~~Some form of concurrency?~~ This turned out to be an awful idea
- [x] A pop of colour 
- [ ] Audio
- [x] Options for IO type
- [ ] Options for resolution?
- [ ] GUI
- [x] Live interpolation
- [ ] Cython static typing?

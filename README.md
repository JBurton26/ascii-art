## CREDITS

Made with Python, based on https://gist.github.com/robert/b0b14b1fd4a5feb2b45ab3ce049f5707

## USAGE

All builds need Python 3.13.

### Windows

Install the required libraries with `pip install -r requirements.txt`. Furthermore, > C++ Build tools 14 needed for cython compilation of functions library.

With these requirements complete, the application can be run with `./run.sh` or `./ascii.py [OPTIONS]`.

### Linux (Tested on Kubuntu 25.10, Dell Latitude 7400)

On Linux, I have found that a virtual environment is needed. To achieve this, commands need to be run in the following order:
```bash
cd ascii-art/
sudo apt install python3.13-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run.sh
```

Once this is run for the first time, the application can be run with `./ascii.py [OPTIONS]`.

#### Note

If the warning for `qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in ...` appears, then the following commands removed the warning message on my machine.

```bash
sudo apt install qtwayland5
export QT_QPA_PLATFORM="xcb"
```

#### Note

On Linux, I have noticed a significant lag between movements and the application updating. The framerate appears to be smooth, just with a delay of approximately a second.

## OPTIONS:

-f, --filename  : Filename of the video file you desire to be processed to ASCII, incompatible with the -wc/--webcam option. When using the `-f` flag, the video output will be found in the `/out` folder. (INPUT: string)

--webcam   : Live processing of video from webcam instead of file.

--invert    : Option for inverting the output.

--colour        : Option for interpreting colour rather than the default green-black monochromatic interpretation.

## TODO:
- ~~Some form of concurrency?~~ This turned out to be an awful idea
- [x] A pop of colour 
- [x] Audio for prerecorded videos.
- [x] Options for IO type
- [ ] Options for resolution?
- [ ] GUI
- [x] Live interpolation
- [ ] Cython static typing?

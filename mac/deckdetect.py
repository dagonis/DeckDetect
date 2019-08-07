'''
DeckDetect for Mac
Author: Kt - github.com/dagonis
Inspired By: https://github.com/beatsbears/pkl
'''
import argparse

from AppKit import NSApplication, NSApp
from Foundation import NSObject
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, _):
        mask_down = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask_down, key_handler)

def key_handler(event, timing_dict = {}):
    threshhold = args.threshhold  # I know I know
    try:
        timing_dict[int(event.timestamp())] = timing_dict.get(int(event.timestamp()), 0) + 1
        if timing_dict[int(event.timestamp())] > threshhold:
            print('HID ATTACK DETECTED')
        for ts in timing_dict.keys():
            # This is some manual GC to keep the timing_dict small
            if not ts == int(event.timestamp()):
                timing_dict.pop(ts)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()
    except Exception as e:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshhold", "-t", default=10, type=int, help="The number of keystrokes to trigger an alert. Default is 10")
    args = parser.parse_args()
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()
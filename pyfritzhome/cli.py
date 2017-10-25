from __future__ import print_function
import logging
import argparse

from pyfritzhome import Fritzhome

_LOGGER = logging.getLogger(__name__)


def list_all(fritz, args):
    """Command that prints all device information."""
    devices = fritz.get_devices()

    for device in devices:
        print('#############')
        print('name=%s' % device.name)
        print('  productname=%s' % device.productname)
        print('  manufacturer=%s' % device.manufacturer)
        print('  ain=%s' % device.ain)
        print('  id=%s' % device.id)
        print('  fw=%s' % device.fw_version)
        print("  present=%s" % device.get_present())

        if device.has_switch:
            print("  switch_state=%s" % device.get_switch_state())
            print("  switch_power=%s" % device.get_switch_power())
            print("  switch_energy=%s" % device.get_switch_energy())

        if device.has_temperature_sensor:
            print("  temperature=%f" % device.get_temperature())

        if device.has_thermostat:
            print("  target=%s" % device.get_target_temperature())
            print("  comfort=%s" % device.get_comfort_temperature())
            print("  eco=%s" % device.get_eco_temperature())

def device_name(fritz, args):
    """Command that prints the device name."""
    print(fritz.get_actor_name(args.ain))

def device_presence(fritz, args):
    """Command that prints the device presence."""
    print(int(fritz.get_actor_present(args.ain)))

def switch_get(fritz, args):
    """Command that get the device switch state."""
    print(fritz.get_switch_state(args.ain))

def switch_on(fritz, args):
    """Command that set the device switch state to on."""
    fritz.set_switch_state_on(args.ain)

def switch_off(fritz, args):
    """Command that set the device switch state to off."""
    fritz.set_switch_state_off(args.ain)

def switch_toggle(fritz, args):
    """Command that toggles the device switch state."""
    fritz.set_switch_state_toggle(args.ain)

def main(args=None):
    """The main function."""
    parser = argparse.ArgumentParser(
        description='Fritz!Box Smarthome CLI tool.')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='be more verbose')
    parser.add_argument('-f', '--fritzbox', type=str, dest='host',
                        help='Fritz!Box IP address', default='fritz.box')
    parser.add_argument('-u', '--user', type=str, dest='user',
                        help='Username')
    parser.add_argument('-p', '--password', type=str, dest='password',
                        help='Username')
    parser.add_argument('-a', '--ain', type=str, dest='ain',
                        help='Actor Identification', default=None)

    _sub = parser.add_subparsers(title='Commands')

    # list all devices
    subparser = _sub.add_parser('list', help='List all available devices')
    subparser.set_defaults(func=list_all)

    # device
    subparser = _sub.add_parser('device', help='Device/Actor commands')
    _sub_switch = subparser.add_subparsers()

    # device name
    subparser = _sub_switch.add_parser('name', help='get the device name')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=device_name)

    # device presence
    subparser = _sub_switch.add_parser('present',
                                       help='get the device presence')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=device_presence)

    # switch
    subparser = _sub.add_parser('switch', help='Switch commands')
    _sub_switch = subparser.add_subparsers()

    # switch get
    subparser = _sub_switch.add_parser('get', help='get state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_get)

    # switch on
    subparser = _sub_switch.add_parser('on', help='set on state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_on)

    # switch off
    subparser = _sub_switch.add_parser('off', help='set off state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_off)

    # switch toggle
    subparser = _sub_switch.add_parser('toggle', help='set off state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_toggle)


    args = parser.parse_args(args)

    logging.basicConfig()
    if args.verbose:
        logging.getLogger('pyfritzhome').setLevel(logging.DEBUG)

    fritzbox = None
    try:
        fritzbox = Fritzhome(host=args.host, user=args.user,
                             password=args.password)
        fritzbox.login()
        args.func(fritzbox, args)
    finally:
        if fritzbox is not None:
            fritzbox.logout()

if __name__ == '__main__':
    main()

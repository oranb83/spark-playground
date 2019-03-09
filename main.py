import argparse

from src.common import Runnable


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate spark parser')
    parser.add_argument('-i', '--input',
                        default='input',
                        help='Input folder')
    parser.add_argument('-o', '--output',
                        default='output',
                        help='Output folder')
    parser.add_argument('-c', '--column',
                        default=None,
                        help='Filter by column: e.g. type')
    parser.add_argument('-v', '--values',
                        default=[],
                        action='append',
                        help='Filter by a list of values with OR: e.g. -v PushEvent -v OtherEvent')
    parser.add_argument('-g', '--graph',
                        default=None,
                        help='Supports: [pie, scatter]')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Show mid work spark content')
    args = parser.parse_args()

    Runnable(args).run()

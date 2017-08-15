import argparse

from archie.Archie import Archie

def main():
    parser = argparse.ArgumentParser(description='Build architecture enforcer.')
    parser.add_argument('--install_headers', dest='install_headers', action='store_true', help='install header files from source paths to build paths')
    parser.add_argument('--show_include_path', dest='source_folder', nargs='?', action='store', help='print the include paths which should be used when compiling source folder')
    parser.add_argument('--config', dest='arch_config', nargs='?', action='store', default='.archie_config', type=str, help='architecture configuration file, defaults to .archie_config')
    parser.add_argument('--arg_prefix', dest='arg_prefix', nargs='?', action='store', default='-I', help='argument prefix to use for includes, defaults to -I')
    parser.add_argument('--third_party_arg_prefix', dest='third_party_arg_prefix', nargs='?', action='store', default='-I', help='argument prefix to use for third party includes, defaults to -I')
    parser.add_argument('--absolute', dest='abs_paths', action='store_true', help='convert all include paths to absolute paths')
    parser.add_argument('--include_folder', dest='include_folder', nargs='?', action='store', type=str, help='build folder where headers are installed to')
    parser.add_argument('--no-third-party', dest='third_party', nargs='?', action='store_false', help='don''t add third-party include paths to the list')
    args = parser.parse_args()

    archie = Archie(args.arch_config, args.include_folder)

    if args.install_headers:
        archie.installHeaderFiles()
    if args.source_folder != None:
        archie.printIncludePath(args.source_folder,
        	                    args.arg_prefix,
        	                    args.third_party,
        	                    args.third_party_arg_prefix)

if __name__ == "__main__":
    main()

from assignment2.main import align
import sys
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--seq1', type=str)
parser.add_argument('--seq2', type=str)
parser.add_argument('--permutations', type=int, default=0)

if __name__ == '__main__':
    args,_ = parser.parse_known_args(sys.argv)
    print(args, args.seq1)
    align(args.seq1, args.seq2, args.permutations)
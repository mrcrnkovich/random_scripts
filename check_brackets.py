# python3

from collections import namedtuple

Bracket = namedtuple("Bracket", ["char", "position"])


def are_matching(left, right):
    return (left + right) in ["()", "[]", "{}"]


def find_mismatch(text):

    opening_brackets_stack = []
    mismatch = []
    
    for i, next in enumerate(text):

        # Process opening bracket, write your code here
        if next in "([{":
            opening_brackets_stack.append((next,i+1))

        # Process closing bracket, write your code here
        if next in ")]}":
            if len(opening_brackets_stack)==0:
                mismatch.append((next,i+1))
            else:
                if are_matching(opening_brackets_stack[-1][0],next):
                    opening_brackets_stack.pop()
                else:
                    mismatch.append(opening_brackets_stack.pop())

    if len(opening_brackets_stack)>0: 
        mismatch.extend(opening_brackets_stack)
        
    return mismatch     

def main():
    text = input()
    mismatch = find_mismatch(text)
    # Printing answer, write your code here
    if len(mismatch) == 0:
        print("Success")
    else:
        for i in mismatch:
            print(i[1])

if __name__ == "__main__":
    main()

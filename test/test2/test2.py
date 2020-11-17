
def main1():
    from test.test1.test_class1 import TestClass1

    t = TestClass1()
    t.test()

if __name__ == '__main__':
    import sys, os

    # sys.path.append('F:\Projects\Reactor\\test')
    # sys.path.append('F:\Projects\Reactor\\test\test1')
    sys.path.append('F:\\Projects\\Reactor\\test')
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    print rootPath
    from test.test1.test_class1 import TestClass1

    t = TestClass1()
    t.test()

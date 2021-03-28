if __name__ == '__main__':
    import sys,os
    sys.path.append(os.path.realpath('.'))
    import pipeline_test
    pipeline_test.run_test()
    print("-------------------------")
    # import logger_test
    # logger_test.run_test()
    print("-------------------------")
    import msg_proto_test
    msg_proto_test.run_test()
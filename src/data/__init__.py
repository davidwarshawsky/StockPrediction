def get_slash():
    platform = sys.platform.lower()
    if "dar" not in platform:
        slash = "\\" # Windows
    else:
        slash = "/" # Linux or Mac
    return slash

def cd_wd():
    """
    Changes to StockPrediction as the working directory
    which is the sources root for any module in a subdirectory.
    :return:
    """
    sources_root = 'StockPrediction'
    slash = get_slash()
    paths = os.getcwd().split(slash) # List of directories
    try:
        target_index = paths.index(sources_root)
        for _ in range(len(paths) - target_index - 1):
            os.chdir('..')
    except ValueError:
        message = "The root <{}> is not valid".format(sources_root)
        raise ValueError(message)

cd_wd()
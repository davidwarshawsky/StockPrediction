def get_model_name(ask=False):
    if ask:
        keys = ['symbol', 'days', 'n_filters', 'filter_width', 'batch_size', 'epochs']
        values = []
        for key in keys:
            values.append(str(input("Please enter desired {}: ".format(key))))
        model_name = "wn&%s&%s&%s&%s&%s&%s" % tuple(values)
    else:
        model_name = "wn&MSFT&10&20&5&2048&100"
    return model_name

def set_model_name(model,symbol:str):
    model_name = "wn&{}&{}&{}&{}&{}&{}".format(symbol, model.days, model.n_filters, model.filter_width,
                                               model.batch_size, model.epochs)
    return model_name
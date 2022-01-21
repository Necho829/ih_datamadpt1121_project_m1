def generate_csv(last_df, file_name):
    last_df.to_csv(file_name)
    print("The output file has been generated under {}".format(file_name))
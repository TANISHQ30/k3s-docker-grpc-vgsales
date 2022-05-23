
def checkSales(event, context):

    row = str(event['data']).strip("b'2")
    processed_line = row.strip('"').strip("'").split(",")
    print(processed_line)
    total = float(processed_line[6]) + float(processed_line[7]) + float(processed_line[8]) + float(processed_line[9])
    print(total)
    if(total == float(processed_line[10])):
        return "True"
    else:
        return "False"
import os
import json
import time

def print_progress(filename, progress, start_time):
    print(
        "{} in {} processed: {} sec.".format(
            progress, filename, time.time() - start_time
        )
    )

def parse_value(v):
  val = None
  if 'arrayValue' in v:
    val = []
    if 'values' in v['arrayValue']:
      for item in v['arrayValue']['values']:
        val.append(parse_value(item))
  elif 'nullValue' in v:  
    val = None
  else:
    val = list(v.values())[0]
  return val

def parse_dataflow_export(directory, output_file, parse_item=None):
    start_time = time.time()
    for filename in os.listdir(directory):
        print("Processing {}".format(filename))
        processed = 0
        loop_time = time.time()

        with open(os.path.join(directory, filename), "r") as r:
            for line in r:
                raw = json.loads(line)
                raw = raw["properties"]
                data = {}
                for k, v in raw.items():
                    data[k] = parse_value(v)
                
                if (parse_item):
                  data = parse_item(data)

                with open(output_file, "a") as w:
                    w.write(json.dumps(data) + "\n")
                processed += 1
                if processed % 10000 == 0:
                    print_progress(filename, processed, loop_time)
                    loop_time = time.time()
        
            print("Done processing {}".format(filename))
            print_progress(filename, processed, loop_time)
    print("Procesed all files in {}sec".format(time.time() - start_time))
                    
                    

        

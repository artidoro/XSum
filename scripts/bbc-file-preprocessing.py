import sys
import os
import json

dm_single_close_quote = u'\u2019' # unicode
dm_double_close_quote = u'\u201d'
END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', dm_single_close_quote, dm_double_close_quote, ")"] # acceptable ways to end a sentence

# We use these to separate the summary sentences in the .bin datafiles
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'
SENTENCE_SPLIT = '<split1>'

bbc_tokenized_stories_dir = "./XSum-Dataset/xsum-preprocessed"

finished_files_dir = "./data-convs2s"
bbc_stories_dir = "./bbc-stories"

# Load JSON File : training, dev and test splits.
with open("./XSum-Dataset/XSum-TRAINING-DEV-TEST-SPLIT-90-5-5.json") as json_data:
  train_dev_test_dict = json.load(json_data)

def read_text_file(text_file):
  lines = []
  with open(text_file, "r") as f:
    for line in f:
      lines.append(line.strip())
  return lines

def fix_missing_period(line):
  """Adds a period to a line that is missing a period"""
  if "@highlight" in line: return line
  if line=="": return line
  if line[-1] in END_TOKENS: return line
  # print line[-1]
  return line + " ."

def get_article_from_file(story_file):
  lines = read_text_file(story_file)

  # Lowercase everything
  lines = [line.lower() for line in lines]

  # Put periods on the ends of lines that are missing them (this is a problem in the dataset because many image captions don't end in periods; consequently they end up in the body of the article as run-on sentences)
  lines = [fix_missing_period(line) for line in lines]

  # Make article into a single string add <split1> between sentences (new compared to XSum original preprocessing)
  article = (" %s " % (SENTENCE_SPLIT)).join(lines)

  return article

def get_abstract_from_file(story_file):
  lines = read_text_file(story_file)

  # Lowercase everything
  lines = [line.lower() for line in lines]

  # Put periods on the ends of lines that are missing them (this is a problem in the dataset because many image captions don't end in periods; consequently they end up in the body of the article as run-on sentences)
  lines = [fix_missing_period(line) for line in lines]

  # Make abstract into a signle string, putting <s> and </s> tags around the sentences
  abstract = ' '.join(["%s %s %s" % (SENTENCE_START, sent, SENTENCE_END) for sent in lines])

  return abstract

def write_to_bin(data_type, out_file_rb, out_file_fs):

  """Reads all the bbids and write them to out file."""
  print "Making text file for bibids listed as %s..." % data_type

  bbcids = train_dev_test_dict[data_type]
  num_stories = len(bbcids)

  rb_foutput = open(out_file_rb, "w")
  fs_foutput = open(out_file_fs, "w")

  for idx,s in enumerate(bbcids):

    if idx % 1000 == 0:
      print "Writing story %i of %i; %.2f percent done" % (idx, num_stories, float(idx)*100.0/float(num_stories))

    # Files
    restbodyfile = bbc_tokenized_stories_dir + "/document/" + s + ".document"
    firstsentencefile = bbc_tokenized_stories_dir + "/summary/" + s + ".summary"


    # Get the strings to write to file
    abstract = get_abstract_from_file(firstsentencefile)
    article = get_article_from_file(restbodyfile)

    # Get the number of <split1> and add it to 400 (that way we are not changing the actual tokens per article).
    article_tokens = article.strip().split()
    split_count = article_tokens.count(SENTENCE_SPLIT)

    article = " ".join(article_tokens[:400 + split_count])

    article_file = open(os.path.join(bbc_stories_dir, str(s) + ".article"), "w")
    abstract_file = open(os.path.join(bbc_stories_dir, str(s) + ".abstract"), "w")

    article_file.write(article)
    abstract_file.write(abstract)

    article_file.close()
    abstract_file.close()


  print "Finished writing file %s, %s\n" %(out_file_rb, out_file_fs)

if __name__ == '__main__':

  # Create some new directories
  if not os.path.exists(finished_files_dir): os.makedirs(finished_files_dir)
  if not os.path.exists(bbc_stories_dir): os.makedirs(bbc_stories_dir)

  # Read the tokenized stories, do a little postprocessing then write to text files
  write_to_bin("test", os.path.join(finished_files_dir, "test.document"), os.path.join(finished_files_dir, "test.summary"))
  write_to_bin("validation", os.path.join(finished_files_dir, "validation.document"), os.path.join(finished_files_dir, "validation.summary"))
  write_to_bin("train", os.path.join(finished_files_dir, "train.document"), os.path.join(finished_files_dir, "train.summary"))


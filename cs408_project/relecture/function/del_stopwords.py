import nltk
from nltk.corpus import stopwords

def del_stopwords(input,output):
    
    delete_words = ['0','1','2','3','4','5','6','7','8','9',
                            '"',':',';','!','@','#','$','%','^','&',
                            '*','(',')','+','-','_','=','{','}','[',']','?',
                            '/','<','>',',','.','|','`','~','"',"'",'\\','\n']

    with open(input, "r") as f:
        data = f.readlines()
        
        word_list = []
        for line in data:
            for word in delete_words:
                line = line.replace(word, " ")

            for word in line.split(" "):
                word_list.append(word)
         
        filtered_words = [word for word in word_list if word not in stopwords.words('english')]

        nf = open(output,"w")
        for word in filtered_words:
            if len(word)>1:
                nf.writelines(word+'\n')

if __name__ == '__main__':
    try: 
        del_stopwords("../../test_sample/2.txt","corpus2.txt")
    except:
        nltk.download('stopwords')
        del_stopwords("../../test_sample/1.txt","corpus1.txt")

#!/usr/bin/python3
#import modules , libraries
#cgi modules
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
input_question = form.getvalue("inputQuestion")
#sql modules
import pymysql
import pymysql.cursors
#nltk modules
import nltk
from nltk.corpus import brown
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import tag

#--- nlp part --  #
#specify the stanford tagger
st = StanfordNERTagger('/Users/Hasna/Desktop/stanford-ner-2016-10-31/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       '/Users/Hasna/Desktop/stanford-ner-2016-10-31/stanford-ner.jar',
                       encoding='utf-8')


#nlp functions 
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'(I|i)$', 'PRP'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; will Extend it according to our own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
#############################################################################


class NPExtractor(object):

    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
 
            if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN" or t[1] == "JJ" or t[1] == "JJR" or t[1] == "NR" or t[1] == "CD"  :
            #if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches

#list of bad and stop words including symbols too
bad_words=["rt","@",".","#","4r5e","5h1t","5hit","a55","anal","anus","ar5e","arrse","arse","ass","ass-fucker","asses","assfucker",
"assfukka","asshole","assholes","asswhole","a_s_s","b!tch","b00bs","b17ch","b1tch","ballbag","balls",
"ballsack","bastard","beastial","beastiality","bellend","bestial","bestiality","bi+ch","biatch",
"bitch","bitcher","bitchers","bitches","bitchin","bitching","bloody","blow job","blowjob","blowjobs","boiolas",
"bollock","bollok","boner","boob","boobs","booobs","boooobs","booooobs","booooooobs","breasts",
"buceta","bugger","bum","bunny fucker","butt","butthole","buttmuch","buttplug","c0ck",
"c0cksucker","carpet muncher","cawk","chink","cipa","cl1t","clit","clitoris","clits","cnut",
"cock","cock-sucker","cockface","cockhead","cockmunch","cockmuncher","cocks","cocksuck ","cocksucked ","cocksucker",
"cocksucking","cocksucks ","cocksuka","cocksukka","cok","cokmuncher","coksucka","coon","cox","crap","cum",
"cummer","cumming","cums","cumshot","cunilingus","cunillingus","cunnilingus","cunt","cuntlick ","cuntlicker ",
"cuntlicking ","cunts","cyalis","cyberfuc","cyberfuck ","cyberfucked ","cyberfucker","cyberfuckers","cyberfucking ","d1ck",
"damn","dick","dickhead","dildo","dildos","dink","dinks","dirsa","dlck","dog-fucker","doggin","dogging",
"donkeyribber","doosh","duche","dyke","ejaculate","ejaculated","ejaculates ","ejaculating ","ejaculatings",
"ejaculation",'ejakulate',"f u c k","f u c k e r","f4nny","fag","fagging","faggitt","faggot","faggs","fagot",
"fagots","fags","fanny","fannyflaps","fannyfucker","fanyy","fatass","fcuk","fcuker","fcuking","feck","fecker",
"felching","fellate","fellatio","fingerfuck","fingerfucked","fingerfucker","fingerfuckers","fingerfucking ",
"fingerfucks ","fistfuck","fistfucked ","fistfucker ","fistfuckers ","fistfucking ","fistfuckings ","fistfucks ",
"flange","fook","fooker","fuck","fucka","fucked","fucker","fuckers","fuckhead","fuckheads","fuckin",
"fucking","fuckings","fuckingshitmotherfucker","fuckme ","fucks","fuckwhit","fuckwit","fudge packer","fudgepacker","fuk","fuker",
"fukker","fukkin","fuks","fukwhit","fukwit","fux","fux0r","f_u_c_k","gangbang","gangbanged ","gangbangs ","gaylord",
"gaysex","goatse","God","god-dam","god-damned","goddamn","goddamned","hardcoresex ","hell","heshe",
"hoar","hoare","hoer","homo","hore","horniest","horny","hotsex","jack-off ","jackoff","jap","jerk-off ",
"jism","jiz ","jizm ","jizz","kawk","knob","knobead","knobed","knobend","knobhead","knobjocky","knobjokey","kock",
"kondum","kondums","kum","kummer","kumming","kums","kunilingus","l3i+ch","l3itch","labia","lmfao","lust","lusting",
"m0f0","m0fo","m45terbate","ma5terb8","ma5terbate","masochist","master-bate","masterb8","masterbat*","masterbat3",
"masterbate","masterbation","masterbations","masturbate","mo-fo",
"mof0","mofo","mothafuck","mothafucka","mothafuckas","mothafuckaz","mothafucked","mothafucker","mothafuckers","mothafuckin","mothafucking "
,"mothafuckings","mothafucks","mother fucker","motherfuck","motherfucked","motherfucker","motherfuckers","motherfuckin","motherfucking",
"motherfuckings","motherfuckka","motherfucks","muff","mutha","muthafecker","muthafuckker","muther","mutherfucker","n1gga","n1gger","nazi",
"nigg3r","nigg4h","nigga","niggah","niggas","niggaz","nigger","niggers ","nob","nob jokey","nobhead","nobjocky","nobjokey","numbnuts",
"nutsack","orgasim ","orgasims ","orgasm","orgasms ","p0rn","pawn","pecker","penis","penisfucker","phonesex","phuck","phuk","phuked",
"phuking","phukked","phukking","phuks","phuq","pigfucker","pimpis","piss","pissed","pisser","pissers","pisses ","pissflaps","pissin ",
"pissing","pissoff ","poop","porn",
"porno","pornography","pornos","prick","pricks ","pron",
"pube","pusse","pussi","pussies","pussy","pussys ","rectum","retard","rimjaw","rimming","s hit","s.o.b.","sadist","schlong","screwing",
"scroat","scrote","scrotum","semen","sex","sh!+","sh!t","sh1t","shag","shagger","shaggin","shagging","shemale","shi+",
"shit","shitdick","shite","shited",
"shitey","shitfuck","shitfull","shithead","shiting","shitings","shits","shitted","shitter","shitters ","shitting","shittings",
"shitty ","skank","slut","sluts","smegma","smut",
"snatch","son-of-a-bitch","spac","spunk","s_h_i_t","t1tt1e5","t1tties","teets","teez","testical","testicle","tit",
"titfuck","tits","titt","tittie5","tittiefucker","titties","tittyfuck","tittywank","titwank",
"tosser","turd","tw4t","twat","twathead","twatty","twunt","twunter","v14gra","v1gra","vagina","viagra",
"vulva","w00se","wang","wank","wanker","wanky","whoar","whore","willies","willy","xrated","xxx"]

#--- get the tweets from the table and proccess them with nlp -- #
#connect to db 

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='tweets',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
#access the table tweets_test
tweet_keywords = []

try:
    
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `tweets_test`"

        cursor.execute(sql)
        results = cursor.fetchall()
        for tweet in results:
            tweet_string = (tweet['tweet']).lower()
            for char in tweet_string:
                if char in " ?.!/;:#@":
                    tweet_string = tweet_string.replace(char,' ')


            tweet_id = tweet['tweet_id']
            #print(tweet_string)
            #extract the question to get only the important keywords
            tweet_extracted = NPExtractor(tweet_string)
            result2 = tweet_extracted.extract()
            #list through each keyword and capitalise it and append it in our input keywords list
            for keyword in result2:
        
                if keyword not in bad_words:
                    #tweet_keywords.append(keyword.title())
                    tweet_keywords.append((tweet_id,keyword.title()))
            #***specify question type (who 'person', where ' place', what 'thing, weather ..etc')

finally:
    pass

#insert keywords and id from tweets into keywords table to compare them with input keywords and create an output
try:

    with connection.cursor() as cursor:
        for keyword in tweet_keywords:
            id_of_tweet = keyword[0]
            keyword_string = keyword[1]
            sql = "INSERT INTO `tweets_keywords` (`tweet_id`, `keyword`) VALUES (%s, %s)"
            cursor.execute(sql, (id_of_tweet, keyword_string))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
finally:
    pass
    #connection.close()
#### ---- input part ----- ####
#take input as the question from user

question = str.lower(input("Enter a question: "))
#question = str.lower(inputQuestion)

if any(question.find(s)>=0 for s in bad_words):
    #print html
     print("I cant answer this question")
elif not question:
    #print html
    print("You have not entered a question")
elif len(question.split()) == 1:
    print("Please ask something useful")
else:
    pass 
        ## plamen, eva u need to start from here

    #list to store input keywords to search for them in the tweets keywords
    input_keywords = []
    #extract the question to get only the important keywords
    question_extracted = NPExtractor(question)
    result = question_extracted.extract()

    #list through each keyword and capitalise it and append it in our input keywords list

    for keyword in result:
       input_keywords.append(keyword.title())
    #***specify question type (who 'person', where ' place', what 'thing, weather ..etc')
    #print(input_keywords)

    keywords = []

    keywords2 = []
    list2 = []
    i=0
    for keywordq in input_keywords:
        if i == 0:
            try:
                with connection.cursor() as cursor:
                # Read a single record
                    sql = "SELECT * FROM `tweets_keywords`"
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for tweet in results:
                        keyword = (tweet['keyword']).lower()
                        tweet_id = tweet['tweet_id']
                        keywords.append((tweet_id, keyword))
                       # print (keyword)
                        #print (keywords)
                    for key in keywords:
                        #print(key)
                        if key not in keywords2:
                            keywords2.append(key)


            finally:
                pass
            i= i+1
            for key in keywords2:
                
                if keywordq.lower() == key[1]:

                    key_id = key[0]
                    
                    #print(i)
                    try:
                        with connection.cursor() as cursor:
                        # Read a single record
                            sql = "SELECT DISTINCT keyword FROM tweets_keywords WHERE tweet_id = %s "
                            cursor.execute(sql, (key_id))
                            results = cursor.fetchall()
                            #print(results)
                            for result in results:
                         
                                np_extractor = NPExtractor(result['keyword'].title())
                                result = np_extractor.extract()
                       
                                if len(result) == 1:
                                    #print('yes')
                                    tokenized_text = word_tokenize((result[0]).title())
                                  
                                    calssified_text = st.tag(tokenized_text)
                                   
                                    list2.append(calssified_text)


                                   
                                else:


                                    calssified_text = st.tag(result)
                             
                                    list2.append(calssified_text)
                                  


                    finally:
                        pass

                    break  
        else:

            break 

    #print(list2)
    person = []
    objects = []
    organisation = []
    location = []
    weather = []

    for item in list2:

        numb_items = len(item)
        #print(numb_items)
        if numb_items>1:
            for item2 in item:
                #print(item2[1])
                if item2[1] == 'PERSON':
                    person.append(item2[0])
                elif item2[1] == 'LOCATION':
                    location.append(item2[0])
                elif item2[1] == 'O':
                    if item2[0] != 'Weather':
                        objects.append(item2[0])
                    else:
                        weather.append(item2[0])
                        #print('yes')
        elif numb_items==0:
            pass
        else:

            
            if item[0][1] == 'PERSON':
                person.append(item[0][0])
            elif item[0][1] == 'LOCATION':
                location.append(item[0][0])
            elif item[0][1] == 'O':
               
                if item[0][0] != 'Weather':
                    objects.append(item[0][0])
                else:
                    weather.append(item[0][0])
                    #print('yes')
            
                    
    if len(weather)>=1:
        print('the weather in cardiff is ' + ' '.join(objects) )

    elif len(person) >=1 or len(objects) >=1 or len(location) >=1:
        print(' '.join(person) + ' is a '+ ' '.join(objects)+' in ' + ' '.join(location))
    else:
        print("I am sorry, i dont have the knowledge for this now")
  


    

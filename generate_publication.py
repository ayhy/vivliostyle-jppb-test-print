# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os, sys
import io
import shlex, subprocess
import json
import re
import codecs

def readJsonConfig(srcjsonfile): #return list of pandoc commands for each file
    with io.open(srcjsonfile, 'r', encoding="utf-8") as srcjson:
        data=json.load(srcjson)
        pandocCommandDict={"pandocpath":data["pandoc"]["path"],"srcAndArg":[],"tempfiles":[]}
    
        # prepare  general args
        ## lua-filters
        luaFilter = [ "--lua-filter=" + scriptfile  for scriptfile in data["pandoc"]["lua-filter"]]

        generalconfig = data["pandoc"]["general_config"]

        ## font args(css or include-in-header)
        fontfamilyStyle = [ (font["arg"] + font["path"]) for font in data["font"]]

        ## create file args (pre-toc pages)
        ### Front matter style args - pretoc
        frontmatterStyle = [ "--css=" + style for style in data["style"]["titlepage"]]
        
        if len(data["frontmatter"]["titlepage"]["output"])>0:
            preToCSrc = os.path.join(data["frontmatter"]["srcdir"], data["frontmatter"]["titlepage"]["src"])
            preToCArg = (["--output=" + data["frontmatter"]["titlepage"]["output"],
                            "--metadata=title:" + data["frontmatter"]["titlepage"]["title"]]
                            + generalconfig
                            + fontfamilyStyle
                            + frontmatterStyle
                            + luaFilter)

            preToCArg = " ".join(preToCArg)
            pandocCommandDict["srcAndArg"] = pandocCommandDict["srcAndArg"] + [{"type":"toc_md","input":preToCSrc, "arg":preToCArg}]

        ## create file args (toc)
        ### Front matter style args - toc
        frontmatterStyle = [ "--css=" + style for style in data["style"]["toc"]]
        if len(data["frontmatter"]["toc"]["output"])>0:
            # creates temporary .md and converts to html
            tocmd="__temp_toc.txt"
            tocmdSrc = [os.path.join(data["body"]["srcdir"], filedata["src"]) for filedata in data["body"]["file"]]
            tocmdSrc = " ".join(tocmdSrc)
            tocmdArg = ["--output=" + tocmd,"--toc",
                        "--toc-depth=" + str(data["frontmatter"]["toc"]["section_depth"]),
                        "--template=" + data["frontmatter"]["toc"]["toc-template"]]
            if len(data["frontmatter"]["toc"]["src_prepend"])>0:
                tocmdArg = tocmdArg + ["--include-before-body=" +
                                       os.path.join(data["frontmatter"]["srcdir"],data["frontmatter"]["toc"]["src_prepend"])]
            if len(data["frontmatter"]["toc"]["src_append"])>0:
                tocmdArg = tocmdArg + ["--include-after-body=" +
                                       os.path.join(data["frontmatter"]["srcdir"],data["frontmatter"]["toc"]["src_append"])]
            tocmdArg = " ".join(tocmdArg)
            pandocCommandDict["srcAndArg"] = pandocCommandDict["srcAndArg"] + [{"type":"toc_md","input":tocmdSrc, "arg":tocmdArg}]

            tochtmlSrc = tocmd
            tochtmlArg = (["--output=" + data["frontmatter"]["toc"]["output"],
                           "--metadata=title:" + data["frontmatter"]["toc"]["title"]]
                            + generalconfig
                            + fontfamilyStyle
                            + frontmatterStyle
                            + luaFilter)
            tochtmlArg = " ".join(tochtmlArg)
            pandocCommandDict["srcAndArg"] = pandocCommandDict["srcAndArg"] + [{"type":"toc","input":tochtmlSrc, "arg":tochtmlArg}]
            pandocCommandDict["tempfiles"] = pandocCommandDict["tempfiles"] + [tocmd]
            

        ## create file args (post-toc pages)
        ### Front matter style args - posttoc
        frontmatterStyle = [ "--css=" + style for style in data["style"]["halftitle"]]
        if len(data["frontmatter"]["halftitle"]["output"])>0:
            tocPostSrc = os.path.join(data["frontmatter"]["srcdir"], data["frontmatter"]["halftitle"]["src"])
            tocPostArg = (["--output=" + data["frontmatter"]["halftitle"]["output"],
                           "--metadata=title:" + data["frontmatter"]["halftitle"]["title"]]
                          + generalconfig
                          + fontfamilyStyle
                          + frontmatterStyle
                          + luaFilter)
            tocPostArg = " ".join(tocPostArg)
            pandocCommandDict["srcAndArg"] = pandocCommandDict["srcAndArg"] + [{"type":"toc","input":tocPostSrc, "arg":tocPostArg}]

        # create file args (body - chapters)
        bodyStyle = [ "--css=" + cssfile for cssfile in data["style"]["body"]]

        for chapter in data["body"]["file"]:
            chapterSrc = os.path.join(data["body"]["srcdir"],chapter["src"])
            
            if not "title" in chapter: # register empty "title" string if "titile" not speficied in src.json
                chapter["title"] = ""
            if not chapter["title"]: #if title is empty string, parse src file and use first header string
                with open(chapterSrc,"r",encoding="utf-8") as bodymd:
                    bodysource = bodymd.read()
                    regex=re.compile("^# [^#].+?\{") #returns header element
                    section_ids=re.findall(regex,bodysource) 
                    chapter["title"] = section_ids[0][2:-1] #uses first header element string

            if not "output" in chapter: # register hogehoge.html from hogehoge.md as output
                chapter["output"] = os.path.splitext(chapter["src"])[0] + ".html"
            chapterArg = (['--metadata title="' + chapter["title"] + '"']
                          + ["--output=" + chapter["output"]]
                          + generalconfig
                          + fontfamilyStyle
                          + bodyStyle
                          + luaFilter)

            chapterArg = " ".join(chapterArg)
            pandocCommandDict["srcAndArg"] = pandocCommandDict["srcAndArg"] + [{"type":"chapter","input":chapterSrc, "arg":chapterArg}]

        # create file args (backmatter -colophan)
        if len(data["backmatter"]["output"])>0:
            backmatterStyle = [ "--css=" + cssfile for cssfile in data["style"]["backmatter"]]
            backSrc =  os.path.join(data["backmatter"]["srcdir"], data["backmatter"]["src"])
            backArg =  (["--output=" + data["backmatter"]["output"],
                         "--metadata=title:" + data["backmatter"]["title"]]
                          + generalconfig
                          + fontfamilyStyle
                          + backmatterStyle
                          + luaFilter)

            backArg = " ".join(backArg)
            pandocCommandDict["srcAndArg"] = pandocCommandDict["srcAndArg"] + [{"type":"backmatter","input":backSrc, "arg":backArg}]

        #create readingorder for webpub
        frontmatterdict = [{"url":data["frontmatter"]["titlepage"]["output"],
                            "name":data["frontmatter"]["titlepage"]["title"],
                            "category":"pre_toc"},
                           {"url":data["frontmatter"]["toc"]["output"],
                            "name":data["frontmatter"]["toc"]["title"],
                            "category":"toc",
                            "rel": "contents",
                            "type": "LinkedResource"},
                           {"url":data["frontmatter"]["halftitle"]["output"],
                            "name":data["frontmatter"]["halftitle"]["title"],
                            "category":"post_toc"}]
        chapterdictlist = [{"url":mychapter["output"],"name":"","category":"body"} for mychapter in data["body"]["file"]]
        backmatterdict = [{"url":data["backmatter"]["output"],"name":data["backmatter"]["title"],"category":"backmatter"}]

        pandocCommandDict["readingOrder"] = frontmatterdict + chapterdictlist + backmatterdict

        #return value should look like:
        # {"pandoc":{
        #     "exepath": "hoge/hoge"
        #     "commandList": ["type":"toc-md", "input":"part1.md part2.md outro.md","arg": "__temp_toc.md --template=../template-TOC-Only.md",
        #                  "type":"frontmatter", "input":"intro.md __temp_toc.md into2.md","arg":"--strip-comments --section-divs -o 00_intro.html -c style.css",
        #                  "type":"body","input":"part1.md","arg":["--strip-comments","--section-divs","-o 01_pt1.html", "-c style.css", "-c style_pagenum.css"],
        #                  "type":"body","input":"part2.md","arg":["--strip-comments","--section-divs","-o 01_pt2.html", "-c style.css", "-c style_pagenum.css"],
        #                  "type":"back","input":"outro.md","arg":["--strip-comments","--section-divs","-o 99_outro.html", "-c style.css"]
        #          ]
        #   },
        #  "webpub_readincOrder":{[
        #  {
        #    url": "01_body.html",
        #    "name": "", #empty at initial setting / updated during tocfix, insert first #href name
        #   },
        #}
    return pandocCommandDict

def subprocess_outputAll(fullcmdinput):
    print(fullcmdinput)
    process=subprocess.Popen(fullcmdinput,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    returncode = process.wait()
    print('returned {0}'.format(returncode))
    print(process.stdout.read())
    print(process.stderr.read())

def buildHtml(pandocCommandDict):
    pandoc_cmd = "pandoc"
    if len(pandocCommandDict["pandocpath"])>0:
        pandoc_cmd = os.path.realpath(os.path.join(pandocCommandDict["pandocpath"],pandoc_cmd))
    print("checking pandoc version")
    fullcmd = pandoc_cmd + " -v"
    subprocess_outputAll(fullcmd)

    for content in pandocCommandDict["srcAndArg"]:
        fullarg = pandoc_cmd + " " + content["input"]  + " " + content["arg"]
        fullarg = fullarg.replace("\\", "/") #windows issue
        subprocess_outputAll(fullarg)
#        try:
#            print( "execute:\n" + fullarg)
#            result=subprocess.run(fullarg,shell=True, check=True)
#            print(result.args)
#           except subprocess.CalledProcessError as e:
#            print("Pandoc Error detected")
#            print(e.output)


#pandoc's  --toc option will generate link to #idname but not file.html#idname.
#using readingOder, files with category:"toc" are updated their link based on files with category:body.
def updateToCLink(configDict):
    print("updating ToC with readingOrder")
#    print(readingOrder)
    readingOrder = configDict["readingOrder"]
    tocpathList=[]
    bodypathList=[]
    replaceList=[]
    for section in readingOrder:
        if section["category"] == "toc":
            tocpathList = tocpathList + [section["url"]]
        elif section["category"] == "body":
            bodypathList = bodypathList + [section["url"]]
            with open(section["url"],"r",encoding="utf-8") as bodyhtml:
                bodysource = bodyhtml.read()
                regex = re.compile("id=[^\n\r\s]+.*?")
                section_ids=re.findall(regex,bodysource)
                section["name"] = section_ids[0][3:-1].replace("'","").replace('"','')

    for bodypath in bodypathList:
        with open(bodypath,"r",encoding="utf-8") as bodyhtml:
            bodysource = bodyhtml.read()
            regex = re.compile("id=[^\n\r\s]+.*?")
            idnameList=re.findall(regex,bodysource)
            for idname in idnameList:
                idname_trim=idname[3:-1].replace("'","").replace('"','')
                replaceList.append({"id":idname_trim,"file":bodypath})
            #collects dict of identifier-filename
            #[{"id":"some-ch-title","file":"bodyfile"}]
            # this will collect all subsections even when not in TOC
            # but only ones available on gets converted so should be fine

    for tocpath in tocpathList:
        with open(tocpath,"r",encoding="utf-8") as tochtml:
            toc_data = tochtml.read()
            for replacePair in replaceList:
                replace_target_dq = 'href="#' + replacePair["id"] + '"'
                replace_result_dq = 'href="' + replacePair["file"] + "#" + replacePair["id"] + '"'
                replace_target_sq = "href='#" + replacePair["id"] + "'"
                replace_result_sq = "href='" + replacePair["file"] + "#" + replacePair["id"] + "'"
                replace_target_nq = "href=#" + replacePair["id"]
                replace_result_nq = "href=" + replacePair["file"] + "#" + replacePair["id"]
#                print ("convert from " + replace_target_dq + " to " + replace_result_dq)
                toc_data = toc_data.replace(replace_target_dq, replace_result_dq)
                toc_data = toc_data.replace(replace_target_sq, replace_result_sq)
                toc_data = toc_data.replace(replace_target_nq, replace_result_nq)

        with open(tocpath,"w",encoding="utf-8") as tochtml:
            tochtml.write(toc_data)
    configDict["readingOrder"] = readingOrder
    return configDict
        
def updatePubJson(configDict):
    readingOrder = configDict["readingOrder"]
    print("updating web publication manifest with readingOrder")
    publication = {"@context": ["https://schema.org","https://www.w3.org/ns/pub-context"],
                   "type": "Book",
                   "conformsTo": "https://github.com/vivliostyle/vivliostyle-cli",
                   "author": "please put your name here",
                   "name": "please put your project name here"}
    if (os.path.exists("publication.json")):
        if os.path.getsize("publication.json") > 0:
            with io.open('publication.json', 'r', encoding="utf-8") as jsonfile:
                publication=json.load(jsonfile)
    publication["readingOrder"] = readingOrder
    
    with open("publication.json", "w", encoding="utf-8") as outfile:
        rawstring = json.dumps(publication,  indent = 2, separators=(',',":"))
        rawstring = codecs.decode(rawstring, "unicode_escape") # convert \u{xxx} -> readable characters
        outfile.write(rawstring)
#        json.dump(publication, outfile, indent = 2, separators=(',',":"))
    return configDict

def deleteTempfiles(configDict):
    if "tempfiles" in configDict:
        for tempfile in configDict["tempfiles"]:
            os.remove(tempfile)

def parseandprocess(args):
    srcjsonfilepath = "src.json"
    if len(args)>1:
        srcjsonfilepath = args[1]
        print(srcjsonfilepath)
        if (len(os.path.dirname(srcjsonfilepath))>0):
            os.chdir(os.path.dirname(srcjsonfilepath))
        srcjsonfilepath=os.path.basename(srcjsonfilepath)

    configDict = readJsonConfig(srcjsonfilepath)
    #print(configDict)
    buildHtml(configDict)
    deleteTempfiles(configDict)
    configDict = updateToCLink(configDict)
    configDict = updatePubJson(configDict)

    print("building html and publication.json complete")

if __name__=='__main__':
    parseandprocess(sys.argv)
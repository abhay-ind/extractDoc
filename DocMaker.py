import os

###
#
#
#  specify the path of the root directory where the java classes are present.
#
#
###
path = "/home/abhay/onos/core"

###
#
#
# specify the output file name
#
#
###
csv = open("api_doc.csv", "w")
finalList = []
packageSet = set()


def listOfJavaFiles(path):
    res = os.listdir(path)
    for each in res:
        try:
            eachList = os.listdir(path + "/" + each)
            if os.path.isdir(path + "/" + each):
                listOfJavaFiles(path + "/" + each)
        except Exception:
            #######
            ##
            ##
            ## Here 'Service' an be replaced with any keyword which defines the set of classes you want to extract documentation of.
            ##
            ##
            #######
            if each.find("Service") != -1:
                #             if each.find("TopologyService") != -1 or each.find("PacketService") != -1 or each.find("FlowRuleService") != -1 or each.find("LinkService") != -1 or each.find("HostService") != -1 or each.find("IntentService") != -1 or each.find("BusService") != -1 or each.find("PathService") != -1 or each.find("DeviceService") != -1 :
                read = open(path + "/" + each, "r")
                wholeCode = read.read()
                lines = wholeCode.split("\n")
                #                 print(wholeCode)
                #                 print(lines)
                count = 0
                packIndx = wholeCode.find("package")

                string = wholeCode[packIndx:]
                package = wholeCode[packIndx : packIndx + string.find(";")]
                for eachLine in lines:
                    if eachLine.find("public interface") != -1:
                        count += 1
                        break
                if count != 0:
                    #                     print(path+"/"+each)
                    #                     print(package)
                    read = open(path + "/" + each, "r")
                    code = read.read()
                    all_functions = code[code.find("{") + 1 :].split("/**")[1:]
                    #                     csv.write("\n\n\n"+each+"\n")
                    packageSet.add(package)
                    for eachFL in all_functions:
                        #                         print(each)
                        funcLines = eachFL.split("\n")
                        comment = eachFL[eachFL.find("*") : eachFL.find("*/")]
                        for char in "/*":
                            comment = comment.replace(char, "")
                        #                         comment=comment.replace("\n","")
                        comment = comment.replace("\t", "")
                        l = comment.split("\n")
                        finalComment = ""
                        for ea in l:
                            if (
                                ea.find("@param") == -1
                                and ea.find("@return") == -1
                                and ea.find("@default") == -1
                                and ea.strip() != ""
                            ):
                                finalComment += ea + "\n"
                        onlyFunction = []
                        for eLine in funcLines:
                            if eLine.find("/") == -1 and eLine.find("*") == -1:
                                onlyFunction.append(eLine)
                        onlylines = ""
                        for eLine in onlyFunction:
                            if eLine.strip() != "":
                                onlylines += eLine.strip()
                        signature = onlylines[: onlylines.find(")") + 1]
                        #                         print(signature)
                        #                         print(each+","+signature+","+comment+"\n")

                        finalList.append([package, each, signature, finalComment])


listOfJavaFiles(path)
# print(packageSet)

###
#
#
# Write into a csv file using '#' as delimiter.
# Package name is also added to demarcate.
# Columns: Function Signature     #     Documentation
#
#
###
for each in packageSet:
    allList = []
    classSet = set()
    for eachLine in finalList:
        if eachLine[0] == each:
            allList.append(eachLine)
            classSet.add(eachLine[1])
    #     print(classSet)
    #     print(allList)
    csv.write(each + "\n")
    for eachClass in classSet:
        csv.write("\n" + eachClass + "\n")
        for temp in allList:
            #             print(temp[0])
            if temp[0] == each and temp[1] == eachClass:
                #                 print("Hello1")
                csv.write(temp[2] + '#"' + temp[3] + '"\n')

import xml.etree.ElementTree as ET

XMLfiles = ["Manifestos/VP_1986.party-topicnr-content.xml",
            "Manifestos/VP_1994.party-topicnr-content.xml",
            "Manifestos/VP_1998.party-topicnr-content.xml"]
for XMLfile in XMLfiles:
  tree = ET.parse(XMLfile)
  year = tree.getroot()
  print(year.attrib['year'])
  for party in year:
    print(party.attrib['party'])
    count_topics = 0
    for topic in party:
      count_topics += 1
      #print(topic.attrib['id'])
      count_themes = 0
      for themes in topic:
        for theme in themes:
          count_themes += 1
          #print(theme.attrib['id'])
        #print("    ",count_themes)
    print("  ",count_topics)


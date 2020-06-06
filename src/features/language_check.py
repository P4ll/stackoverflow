import language_check
tool = language_check.LanguageTool('en-US')
text = u'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
matches = tool.check(text)
len(matches)
def Comma_splitter(tag_string):
    return [t.strip().lower() for t in tag_string.split(',') if t.strip()]


def Comma_joiner(tags):
    return ', '.join(t.name for t in tags)

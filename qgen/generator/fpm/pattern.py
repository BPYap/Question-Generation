# **************************************************************************************************
# Tokens and their meaning:
# 1. <obj>  : object (includes time and place)
# 2. <sbj>  : subject
# 3. <act>  : action (must begin with verb)
# 4. <st>   : statement/short phrase describing a situation (can form complete sentence by itself)
# **************************************************************************************************

TOKENS = ['<sbj>', '<obj>', '<act>', '<st>']

pattern_specs = [
    # yes/no question (existential)
    {
        "patterns": [
            "{aux1} there <obj>",
            "{aux1} there any <obj>",
            "{aux2} there be <obj>",
            "{aux2} there be any <obj>",
            "Any <obj>"
        ],
        "substitution_keys": {"aux1": ['is', 'are'], "aux2": ['will', 'would']},

        "description": "yes/no question (existential)"
    },

    # yes/no question (obligatory)
    {
        "patterns": [
            "Is it {necessary} for <sbj> to <act>",
            "Is it {necessary} to <act>",
            "{pre-if} <st> Is it {necessary} for <sbj> to <act>",
            "Is it {necessary} for <sbj> to <act> {if} <st>",
            "{aux1} <sbj> {required} to <act>",
            "{pre-if} <st> {aux1} <sbj> {required} to <act>",
            "{aux2} <sbj> {need} to <act>",
            "{aux2} <sbj> {need} to <act> {if} <st>",
            "{pre-if} <st> {aux2} <sbj> {need} to <act>",
            "{aux3} <sbj> <act>",
            "{pre-if} <st> {aux3} <sbj> <act>",
            "<st> {aux3} <sbj> <act>",
        ],
        "substitution_keys": {
            "necessary": ['necessary', 'compulsory', 'required', 'obligatory'],
            "required": ['required', 'obliged'],
            "if": ['if', 'when'],
            "pre-if": ['if', 'when', ''],
            "need": ["have", "need", "still need", "still have"],
            "aux1": ['is', 'am', 'are'],
            "aux2": ['do', 'does'],
            "aux3": ['must', 'should', 'shall']
        },

        "description": "yes/no question (obligatory)"
    },

    # yes/no question (location)
    {
        "patterns": [
            "{aux} <st> possible {within} <obj>",
        ],
        "substitution_keys": {"aux": ['is', 'are'], "within": ['within', 'inside', 'in']},

        "description": "yes/no question (location)"
    },

    # generic yes/no question (conditional)
    {
        "patterns": [
            "{aux} <st>",
            "Am I right to say that <st>",

            "<st> {true}",
        ],
        "substitution_keys": {
            "aux": ['do', 'does'],
            "true": ["True", "True or False", "Really", "Ya meh", "Is it true", "True or not"]
        },

        "description": "generic yes/no question (conditional)"
    },

    # yes/no question (conditional)
    {
        "patterns": [
            "If <st> {aux1} <sbj> <act>",
            "<st> {aux1} <sbj> <act>",
            "{aux2} there <obj> where <st>",
            "{aux1} <sbj> <act> if <st>",
            "{aux3} there be <obj> if <st>",

            "For <st> {aux2} there <obj>",
            "For <st> got <obj>",
            "Given <st> got <obj>",
        ],
        "substitution_keys": {"aux1": ['do', 'does'], "aux2": ['is', 'are'], "aux3": ['will', 'would']},

        "description": "yes/no question (conditional)"
    },

    # yes/no question (post-conditional)
    {
        "patterns": [
            "After <st> {aux1} <sbj> {need} to <act>",

            "{aux1} <sbj> {need} to <act> after <st>",
        ],
        "substitution_keys": {"aux1": ['do', 'does'], "need": ['have', 'still have', 'need', 'still need']},

        "description": "yes/no question (post-conditional)"
    },

    # can/cannot question
    {
        "patterns": [
            "{aux1} <sbj> <act>",
            "{aux2} <sbj> {allowed} to <act>",
            "Is it {possible} for <sbj> to <act>",
            "Is it {possible} if <sbj> <act>",
            "Is it {possible} to <act>",
            "{aux2} <sbj> able to <act>",
            "Can <st>",
        ],
        "substitution_keys": {
            "allowed": ['allowed', 'entitled'],
            "possible": ['possible', 'alright', 'ok'],
            "aux1": ['can', 'could', 'may'],
            "aux2": ['am', 'is', 'are'],
        },

        "description": "can/cannot question"
    },

    # can/cannot question (two actions)
    {
        "patterns": [
            "{aux1} <sbj> <act> {to} <act>",
        ],
        "substitution_keys": {
            "aux1": ['can', 'could'],
            "to": ['to be', 'which is to be'],
        },

        "description": "can/cannot question (two actions)"
    },

    # can/cannot question (role play)
    {
        "patterns": [
            "{aux1} <sbj> working as <obj> <act>",

            "As <obj> , {aux1} <sbj> <act>",
        ],
        "substitution_keys": {"aux1": ['can', 'could']},

        "description": "can/cannot question (role play)"
    },

    # can/cannot question (conditional)
    {
        "patterns": [
            "<st> Is it possible for <sbj> to <act>",
            "{if} <st> Is it possible for <sbj> to <act>",
            "<st> {aux1} <sbj> <act>",
            "{if} <st> {aux1} <sbj> <act>",
            "{aux1} <sbj> <act> {if} <st>",
            "<st> May I know if <obj> {aux1} <act>",
            "{if} <st> May I know if <obj> {aux1} <act>",
            "{aux2} <sbj> allowed to <act> if <st>",
            "I understand that <st> but {aux1} <sbj> <act>",
            "I understand that <st> However, {aux1} <sbj> <act>",
        ],
        "substitution_keys": {
            "aux1": ['can', 'could', 'may'],
            "aux2": ['am', 'is', 'are'],
            "if": ['if', 'when', 'while'],
        },

        "description": "can/cannot question (conditional)"
    },

    # can/cannot question (post-conditional)
    {
        "patterns": [
            "Is it possible to <act> {after} <st>",
            "{aux} <sbj> <act> {after} <st>",
        ],
        "substitution_keys": {
            "aux": ['can', 'could'],
            "after": ['after', 'now that'],
        },

        "description": "can/cannot question (post-conditional)"
    },

    # can it be question
    {
        "patterns": [
            "{aux} <sbj> be <act>",
            "{aux} <sbj> be <obj>",

            "{aux} <obj> be <sbj>",
        ],
        "substitution_keys": {"aux": ['can', 'could']},

        "description": "can it be question"
    },

    # what question
    {
        "patterns": [
            "What {aux1} <obj>",
            "<st> What {aux1} <obj>",
            "{description} <obj>",
            "What {aux2} <obj> <act>",
            "What {aux1} <obj> all about",
            "What is meant by <obj>",
            "What {aux2} <obj> mean",
            "What <obj> {aux2} <sbj> {need} to <act>",
            "<st> What <obj> {aux2} <sbj> {need} to <act>",
            "What <obj>"
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does'],
            "description": ["Can you tell me more about",
                            "Can you tell me the details about",
                            "May I know about",
                            "I want to know about",
                            "Explain to me"],
            "need": ['need', 'required']
        },

        "description": "what question"
    },

    # what question (capability)
    {
        "patterns": [
            "What {aux1} <sbj> <act>",
            "What <obj> {aux1} <sbj> <act>",
            "What <obj> {aux1} <sbj> <act> as <st>",
        ],
        "substitution_keys": {
            "aux1": ['can', 'could', 'should', 'shall', 'do', 'does'],
            "aux2": ['do', 'does'],
        },

        "description": "what question (capability)"
    },

    # what question (location)
    {
        "patterns": [
            "What {aux} <sbj> do at <obj>",
        ],
        "substitution_keys": {"aux": ['can', 'could']},

        "description": "what question (location)"
    },

    # what question (example)
    {
        "patterns": [
            "{description} <obj>",
        ],
        "substitution_keys": {
            "description": ["Any examples of",
                            "Can you give me overview on",
                            "Give some examples of"]
        },

        "description": "what question (example)"
    },

    # what question (options)
    {
        "patterns": [
            "What <obj> {aux1} available",
            "What <obj> {aux2} <sbj> offers",
            "What <obj> {aux1} {offer} <sbj>",
            "What {aux1} <obj> {offer} <sbj>",
            "What kind of <obj> {aux2} <sbj> offer",

            "What are the options for <obj>",
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does'],
            "offer": ["available in", "offered in", "offered by", 'available on']
        },

        "description": "what question (options)"
    },

    # what question (difference)
    {
        "patterns": [
            "What {aux1} {difference} <obj> {and} <obj>",
            "How {aux1} <obj> different",
            "How {aux2} <obj> differ from <obj>",
            "How {aux1} <obj> different from <obj>",
            "<st> how {aux2} <obj> fare compared to <obj>",
            "{difference} <obj> {and} <obj>",
            "<obj> {and} <obj> got what difference",
            "<obj> {and} <obj> got difference meh",
            "Compare <obj> {and} <obj>",
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does'],
            "difference": ["the difference between",
                           "the main difference between",
                           "Difference between",
                           ],
            "and": ['and', '&', 'vs']
        },

        "description": "what question (difference)"
    },

    # comparison (similarity)
    {
        "patterns": [
            "{aux1} there any similarities between <obj> {and} <obj>",

            "How {aux2} <obj> related to <obj>",
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does'],
            "and": ['and', '&', 'vs']
        },

        "description": "comparison (similarity)"
    },

    # what question (conditional)
    {
        "patterns": [
            "What {aux1} <obj> for <st>",
            "What <obj> {aux2} <sbj> {need} to <act> for <st>",

            "For <st> , what {aux1} <obj>",
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does'],
            "need": ['need', 'have to do']
        },

        "description": "what question (conditional)"
    },

    # how to question
    {
        "patterns": [
            "How to <act>",
            "Where {aux1} <sbj> <act>",
            "Where {aux2} <sbj> <act>",
            "How {aux2} <sbj> <act>",
            "How {aux1} <sbj> <act>",
            "What {aux2} <sbj> {need} to <act>",
            "How <act>"
        ],
        "substitution_keys": {
            "aux1": ['can', 'could', 'should', 'shall'],
            "aux2": ['do', 'does'],
            "need": ['need', 'have to do']
        },

        "description": "how to question"
    },

    # how to question (role play)
    {
        "patterns": [
            "What {aux} <sbj> {need} as <obj> {while} <st>",
        ],
        "substitution_keys": {
            "aux": ['do', 'does'],
            "need": ['need to do', 'have to do'],
            "while": ['while', 'if']
        },

        "description": "how to question (role play)"
    },

    # how to question (conditional)
    {
        "patterns": [
            "<st> How {aux1} <sbj> <act>",
            "{if} <st> How {aux1} <sbj> <act>",
            "How to <act> if <st>",
            "<st> {description}",
            "{if} <st> {description}",
            "What to do if <st>",
            "What {aux1} <sbj> do if <st>",
            "<st> What {aux1} <sbj> do to <act>",
            "{if} <st> What {aux1} <sbj> do to <act>",
            "<st> Where {aux1} <sbj> <act>",
            "{if} <st> Where {aux1} <sbj> <act>",
            "<st> How {aux1} <sbj> <act>",
            "{if} <st> How {aux1} <sbj> <act>",
            "<st> How <sbj> {aux1} <act>",
            "{if} <st> How <sbj> {aux1} <act>",
            "<st> what {aux1} <sbj> do if <st>",
            "{if} <st> what {aux1} <sbj> do if <st>",
            "What {aux1} <sbj> do when <sbj> <act>",
            "{description} {if} <st>",
            "What {aux1} I do in the event <st>",
            "<st> I wish to <act> {description}",
            "{if} <st> I wish to <act> {description}",
            "<st> What {aux1} <sbj> do",
            "{if} <st> What {aux1} <sbj> do",
            "<st> Can you {advise} me on how to <act>",
            "{if} <st> Can you {advise} me on how to <act>",
            "<st> Can you {advise} me how to <act>",
            "{if} <st> Can you {advise} me how to <act>",
            "What else do <sbj> need to do to <act>",
            "<st> Could you help me <act>",
            "{if} <st> Could you help me <act>",
            "What {aux1} I do {if} <st>",
        ],
        "substitution_keys": {
            "aux1": ['can', 'could', 'should', 'shall', 'do', 'does'],
            "description": ["What is the procedure",
                            "What are your suggestions",
                            "What is your advice",
                            "Can you help me",
                            "Could you help me",
                            "What do I have to do",
                            "Can you tell me what to do",
                            "what can I do",
                            "Could you help"
                            ],
            "advise": ["advise", "guide", "please advise", "please guide"],
            "if": ['if', 'while', 'when']
        },

        "description": "how to question (conditional)"
    },

    # how to question (post-conditional)
    {
        "patterns": [
            "How {aux} <sbj> <act> after <st>",
            "What {aux} <sbj> {have} to do after <st>",
        ],
        "substitution_keys": {"aux": ['do', 'does'], "have": ['have', 'need']},

        "description": "how to question (post-conditional)"
    },

    # how stuff works question
    {
        "patterns": [
            "How {aux1} <obj> <act>",
            "How <obj> works",
            "How <obj> {aux1} <act>",
            "How {aux1} <obj> <act> for <obj>",
        ],
        "substitution_keys": {"aux1": ['is', 'are'], "aux2": ['do', 'does']},

        "description": "how stuff works question"
    },

    # how positive question
    {
        "patterns": [
            "How {good} {aux} <obj>",
            "{aux} <obj> {good}",
            "What {aux} so great about <obj>",
            "Can you tell me how {good} {aux} <obj>",
            "Explain how {good} {aux} <obj>"
        ],
        "substitution_keys": {
            "aux": ['is', 'are'],
            "good": ['good', 'well recognised', 'internationally recognised']
        },

        "description": "how positive question"
    },

    # how long question
    {
        "patterns": [
            "How long {aux3} <sbj> be <act>",
            "How long {aux2} <obj> <act>",
            "How long {aux3} <obj> <act>",
            "How long {aux1} <obj>",
            "What is the duration for <obj>",
            "How long <obj>"
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does'],
            "aux3": ['can', 'should', 'will', 'would'],
        },

        "description": "how long question"
    },

    # how much question
    {
        "patterns": [
            "How {much} {aux1} <obj>",
            "How {much} {aux3} <sbj> <act>",
            "How {much} <obj> {aux2} <sbj> <act>",
            "How {much} <obj> {aux2} <sbj> {has}",
            "How {much} <obj>",
            "How {much} <obj> {aux1} there in <sbj>",
            "How {much} <obj> {aux1} there for <st>",

            "What is the amount of <obj>",
            "How {much} <obj>",
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does'],
            "aux3": ['can', 'should', 'will', 'would'],
            "much": ['much', 'many'],
            "has": ['has', 'have'],
        },

        "description": "how much question"
    },

    # why question I
    {
        "patterns": [
            "Why <act>",
            "<st> Why",
            "Why {aux} <sbj> <act>",
            "Why {aux} <st>",
            "<st> Why is {this} so",
            "Why is it that <st>",
            "<st> may I know why is {this} so",
            "Why <sbj> <act>",

            "<st> may I know why",
            "<st> what should I do"
        ],
        "substitution_keys": {
            "aux": ['am', 'is', 'are', 'do', 'does'],
            "this": ['this', 'that']
        },

        "description": "why question I"
    },

    # why question II
    {
        "patterns": [
            "Why {aux} <sbj> <act>",
        ],
        "substitution_keys": {"aux": ['can', 'should', 'will', 'would']},

        "description": "why question II"
    },

    # why cannot question
    {
        "patterns": [
            "Why {aux} <sbj> {cannot} <act>",
            "Why <sbj> {cannot} <act> when <st>",
            "After <st> why {aux} <sbj> {cannot} <act>",
            "Why can not <sbj> <act>",

            "Why {cannot} <act>",
        ],
        "substitution_keys": {
            "aux": ['am', 'is', 'are'],
            "cannot": ['cannot', 'unable to']
        },

        "description": "why cannot question"
    },

    # where is question
    {
        "patterns": [
            "Where {aux1} <obj>",
            "Where {aux2} <sbj> find the procedure to <act>",
            "Where to <act>",
            "Where <obj>"
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['can', 'could']
        },

        "description": "where is question"
    },

    # who is question
    {
        "patterns": [
            "Who {aux2} <act>",
            "Who {aux1} <sbj>",
            "Who <act>",
            "Who {aux1} <st>",
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['can', 'could', 'should', 'shall', 'will', 'would'],
        },

        "description": "who is question"
    },

    # who does question
    {
        "patterns": [
            "Who {aux} <obj> <act>",
        ],
        "substitution_keys": {
            "aux": ['do', 'does']
        },

        "description": "who does question"
    },

    # who can I contact question
    {
        "patterns": [
            "Whom {aux2} <sbj> <act> regarding <obj>",
            "Who {aux2} <sbj> <act> regarding <obj>",
            "Who {aux1} <sbj> <act> if <st>",
            "Who {aux2} <sbj> <act> if <st>",
            "<st> who {aux2} <sbj> approach",
            "Who {aux2} I talk to about <obj>",
            "If <st> whom can <sbj> <act>",
            "Who {aux1} I <act> regarding <obj>",
            "Who {aux2} assist me if <st>",
            "Who {aux2} <sbj> contact regarding <obj>",
            "Who {aux2} <sbj> ask for assistance if <st>",
        ],
        "substitution_keys": {
            "aux1": ['do', 'does'],
            "aux2": ['can', 'could', 'should', 'shall']
        },

        "description": "who can I contact question"
    },

    # which question
    {
        "patterns": [
            "Which <obj> {aux} <act>",
            "Which <obj> <act>",
            "Which <obj>"
        ],
        "substitution_keys": {"aux": ['will', 'would', 'can', 'could']},

        "description": "which question"
    },

    # which to use question
    {
        "patterns": [
            "<st> {which} <obj> {aux1} <sbj> <act>",
            "{which} <obj> {aux1} <sbj> <act>",
            "<st> {which} {aux2} <obj>"
        ],
        "substitution_keys": {
            "aux1": ['do', 'does', 'can', 'could', 'should', 'shall'],
            "aux2": ['is', 'are'],
            "which": ['which', 'what']
        },

        "description": "which to use question"
    },

    # when question
    {
        "patterns": [
            "When {aux1} <obj>",
            "When {aux1} <obj> if <st>",
            "When {aux2} <sbj> <act>",
            "<st> When {aux2} <sbj> <act>",
            "When {aux3} be <obj>",
            "When <obj>"
        ],
        "substitution_keys": {
            "aux1": ['is', 'are'],
            "aux2": ['do', 'does', 'can', 'could', 'should', 'shall'],
            "aux3": ['will', 'would']
        },

        "description": "when question"
    },

    # when question (begin)
    {
        "patterns": [
            "What time {aux} <obj> {start}",
            "When {aux} <obj> {start}",
        ],
        "substitution_keys": {
            "aux": ['do', 'does', 'will', 'would'],
            "start": ['start', 'open'],
        },

        "description": "when question (begin)"
    },

    # when question (end)
    {
        "patterns": [
            "What time {aux} <obj> close",
            "Is there {deadline} for <obj>",
        ],
        "substitution_keys": {
            "aux": ['do', 'does', 'will', 'would'],
            "deadline": ['deadline', 'a deadline', 'closing date', 'a closing date'],
        },

        "description": "when question (end)"
    },

    # when question (obligatory)
    {
        "patterns": [
            "When {aux} <sbj> <act>",
        ],
        "substitution_keys": {"aux": ['must', 'should', 'do', 'does']},

        "description": "when question (obligatory)"
    },

    # request question
    {
        "patterns": [
            "<st> {aux} you <act>",
            "{aux} you <act>",
        ],
        "substitution_keys": {
            "aux": ['can', 'could', 'will', 'would'],
        },

        "description": "request question"
    },

    # hypothetical question
    {
        "patterns": [
            "What if <sbj> <act>",
            "What if <st>",

            "If <st> then how",
            "If <sbj> <act> then how",
        ],
        "substitution_keys": {},

        "description": "hypothetical question"
    },

    # yes/no question (future tense)
    {
        "patterns": [
            "{aux} <sbj> <act> if <st>",
            "{aux} <sbj> <act>",
            "<st> {aux} <sbj> <act>",
        ],
        "substitution_keys": {"aux": ['will', 'would']},

        "description": "yes/no question (future tense)"
    },

    # can/cannot question (future tense)
    {
        "patterns": [
            "If <st> {aux} <sbj> <act>",
        ],
        "substitution_keys": {"aux": ['will', 'would']},

        "description": "can/cannot question (future tense)"
    },

    # what question (future tense)
    {
        "patterns": [
            "What <obj> {aux} <sbj> <act>",
            "I wish to know what <obj> {aux} be equivalent to <obj>",
        ],
        "substitution_keys": {"aux": ['will', 'would']},

        "description": "what question (future tense)"
    },

    # how question (future tense)
    {
        "patterns": [
            "How {aux} <sbj> <act>",
            "<st> so how {aux} be <obj> <act>",
            "Under what circumstances {aux} <sbj> <act>",
            "How do <sbj> <act> if <st>",
            "<st> How {aux} <sbj> <act>",
        ],
        "substitution_keys": {"aux": ['will', 'would']},

        "description": "how question (future tense)"
    },

    # how many question (future tense)
    {
        "patterns": [
            "How {much} <obj> {aux} <sbj> <act>",
        ],
        "substitution_keys": {"aux": ['will', 'would'], "much": ['much', 'many']},

        "description": "how many question (future tense)"
    },

    # where question (future tense)
    {
        "patterns": [
            "Where {aux} <obj> <act>",
        ],
        "substitution_keys": {"aux": ['will', 'would']},

        "description": "where question (future tense)"
    },

    # when question (future tense)
    {
        "patterns": [
            "If <st> when {aux} <sbj> <act>",
            "<st> when {aux} <sbj> <act>",
            "When {aux} <sbj> <act>",
        ],
        "substitution_keys": {"aux": ['will', 'would']},

        "description": "when question (future tense)"
    },

    # prediction question (future tense)
    {
        "patterns": [
            "What {aux} happen to <obj>",
            "What {aux} happen to <obj> when <st>",
        ],
        "substitution_keys": {"aux": ['will', 'would']},

        "description": "prediction question (future tense)"
    },

    # when question (past tense)
    {
        "patterns": [
            "When {aux} <obj> <act>",

            "Since when {aux} <obj> <act>",
        ],
        "substitution_keys": {"aux": ['was', 'were']},

        "description": "when question (past tense)"
    }
]

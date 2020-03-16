# Warren Han, Joon Ho Kim , Anne Farley
# CSE 163, Mentor: Wen Qiu
# Class to be used to switch US state IDs to their representative names.
# add() allows users to convert additional state IDs into names if not
# originally provided in the dictionary


class IdSwitch:
    def __init__(self, states):
        """
        Uses dictionary found @ https://gist.github.com/rogerallen/1583593
        to convert a series of state IDs to their full names
        """
        self._dict = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming',
        }
        self._states = states

    def add(self, id, name):
        """
        Allows for user to add a full name for a given ID, if not originally
        in the provided dictionary.
        """
        self._dict[id] = name

    def switch(self):
        """
        Uses the above dictionary to switch ID strings into their
        corresponding state name
        """
        for state in self._states:
            self._states[self._states == state] = self._dict[state]
        return self._states

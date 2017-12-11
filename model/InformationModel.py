class InformationModel:
    """
    Historic of HTTP request
    filled every 10sec with a new list of request ask in the last 10 sec
    So historic is a list of list of w3c-format-string
    """

    def __init__(self):
        self.sections = {}
        self.ip = {}
        self.users = {}

    def set_sections(self, sections):
        if not isinstance(sections, dict):
            raise BaseException("InformationModel : set_sections wrong entry {}".format(sections))
        self.sections = dict(sections)

    def get_sections_info(self):
        return self.sections

    def set_ips(self, ip):
        if not isinstance(ip, dict):
            raise BaseException("InformationModel : set_ip wrong entry {}".format(ip))
        self.ip = dict(ip)

    def get_ips_info(self):
        return self.ip

    def set_users(self, users):
        if not isinstance(users, dict):
            raise BaseException("InformationModel : set_users wrong entry {}".format(users))
        self.users = dict(users)

    def get_users_info(self):
        return self.users

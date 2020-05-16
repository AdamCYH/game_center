from django.views import View


class FiveInARowView(View):
    # get request, return the template
    def get(self, request):
        pass

    def post(self, request):
        pass


def access_game(request, game_id):
    pass


def start_new_game(name, user_id):
    pass

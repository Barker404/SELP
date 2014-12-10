from django.shortcuts import render

def startBattleView(request):
    return render(request, 'battles/startBattle.html')

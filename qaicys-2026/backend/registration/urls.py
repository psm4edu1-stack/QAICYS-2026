from django.urls import path

from . import views


app_name = "registration"

urlpatterns = [
    path("pitch-perfect/", views.PitchPerfectCreateView.as_view(), name="pitch-perfect"),
    path("bid-byte/", views.BidByteCreateView.as_view(), name="bid-byte"),
    path("promptoopia/", views.PromptoopiaCreateView.as_view(), name="promptoopia"),
    path("pixel-cipher/", views.PixelCipherCreateView.as_view(), name="pixel-cipher"),
    path("synapse/", views.SynapseCreateView.as_view(), name="synapse"),
    path("henna-hues/", views.HennaHuesCreateView.as_view(), name="henna-hues"),
    path("palette-pop/", views.PalettePopCreateView.as_view(), name="palette-pop"),
    path("click-craft/", views.ClickCraftCreateView.as_view(), name="click-craft"),
    path("the-verdict/", views.TheVerdictCreateView.as_view(), name="the-verdict"),
    path("estrella/", views.EstrellaCreateView.as_view(), name="estrella"),
    path("unscripted/", views.UnscriptedCreateView.as_view(), name="unscripted"),
    path("battle-zone/", views.BattleZoneCreateView.as_view(), name="battle-zone"),
]

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import (
    BattleZoneRegistration,
    BidByteRegistration,
    ClickCraftRegistration,
    EstrellaRegistration,
    HennaHuesRegistration,
    PalettePopRegistration,
    PitchPerfectRegistration,
    PixelCipherRegistration,
    PromptoopiaRegistration,
    SynapseRegistration,
    TheVerdictRegistration,
    UnscriptedRegistration,
)
from .serializers import (
    BattleZoneSerializer,
    BidByteSerializer,
    ClickCraftSerializer,
    EstrellaSerializer,
    HennaHuesSerializer,
    PalettePopSerializer,
    PitchPerfectSerializer,
    PixelCipherSerializer,
    PromptoopiaSerializer,
    SynapseSerializer,
    TheVerdictSerializer,
    UnscriptedSerializer,
)
from .constraints import registration_submission_guard


class RegistrationCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        with registration_submission_guard():
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"success": False, "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
        return Response(
            {"success": True, "message": "Registration submitted successfully."},
            status=status.HTTP_201_CREATED,
        )


class PitchPerfectCreateView(RegistrationCreateView):
    queryset = PitchPerfectRegistration.objects.all()
    serializer_class = PitchPerfectSerializer


class BidByteCreateView(RegistrationCreateView):
    queryset = BidByteRegistration.objects.all()
    serializer_class = BidByteSerializer


class PromptoopiaCreateView(RegistrationCreateView):
    queryset = PromptoopiaRegistration.objects.all()
    serializer_class = PromptoopiaSerializer


class PixelCipherCreateView(RegistrationCreateView):
    queryset = PixelCipherRegistration.objects.all()
    serializer_class = PixelCipherSerializer


class SynapseCreateView(RegistrationCreateView):
    queryset = SynapseRegistration.objects.all()
    serializer_class = SynapseSerializer


class HennaHuesCreateView(RegistrationCreateView):
    queryset = HennaHuesRegistration.objects.all()
    serializer_class = HennaHuesSerializer


class PalettePopCreateView(RegistrationCreateView):
    queryset = PalettePopRegistration.objects.all()
    serializer_class = PalettePopSerializer


class ClickCraftCreateView(RegistrationCreateView):
    queryset = ClickCraftRegistration.objects.all()
    serializer_class = ClickCraftSerializer


class TheVerdictCreateView(RegistrationCreateView):
    queryset = TheVerdictRegistration.objects.all()
    serializer_class = TheVerdictSerializer


class EstrellaCreateView(RegistrationCreateView):
    queryset = EstrellaRegistration.objects.all()
    serializer_class = EstrellaSerializer


class UnscriptedCreateView(RegistrationCreateView):
    queryset = UnscriptedRegistration.objects.all()
    serializer_class = UnscriptedSerializer


class BattleZoneCreateView(RegistrationCreateView):
    queryset = BattleZoneRegistration.objects.all()
    serializer_class = BattleZoneSerializer

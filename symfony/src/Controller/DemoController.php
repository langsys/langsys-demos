<?php

namespace App\Controller;

use App\Support\LangsysClientFactory;
use DateTimeImmutable;
use Langsys\Symfony\LangsysTranslator;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

class DemoController extends AbstractController
{
    #[Route('/', name: 'demo')]
    public function __invoke(Request $request, LangsysTranslator $langsys): Response
    {
        $count = max(0, min(99, (int) $request->query->get('count', 3)));

        $locales = [
            'en-US' => 'English',
            'es-ES' => 'Español',
            'fr-FR' => 'Français',
            'de-DE' => 'Deutsch',
        ];

        // The bundle's LocaleSubscriber already ran: ?locale= / cookie /
        // session / Accept-Language resolved into the request locale. Fall
        // back to en-US for the pill state when nothing matched (e.g. a first
        // visit with an unsupported locale).
        $active = 'en-US';
        foreach (array_keys($locales) as $code) {
            if (strcasecmp($code, $request->getLocale()) === 0) {
                $active = $code;
                break;
            }
        }

        return $this->render('demo.html.twig', [
            'count' => $count,
            'locales' => $locales,
            'active' => $active,
            'banner' => LangsysClientFactory::bannerState(),
            // The translator works anywhere in PHP — controllers, services,
            // commands, mailers. Computed here so the card shows a
            // server-side result, not a Twig function.
            'orderTitle' => $langsys->translate('Order confirmed', 'Checkout'),
            'orderBody' => $langsys->translate('Your order {id} ships on {date}.', 'Checkout', [
                'id' => '48213', // a string, so it skips number formatting
                'date' => new DateTimeImmutable('2026-08-15'), // locale-formatted
            ]),
        ]);
    }
}

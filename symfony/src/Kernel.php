<?php

namespace App;

use Symfony\Bundle\FrameworkBundle\Kernel\MicroKernelTrait;
use Symfony\Component\DependencyInjection\Loader\Configurator\ContainerConfigurator;
use Symfony\Component\HttpKernel\Kernel as BaseKernel;
use Symfony\Component\Routing\Loader\Configurator\RoutingConfigurator;

class Kernel extends BaseKernel
{
    use MicroKernelTrait;

    public function registerBundles(): iterable
    {
        foreach (require $this->getProjectDir() . '/config/bundles.php' as $class => $envs) {
            if ($envs[$this->environment] ?? $envs['all'] ?? false) {
                yield new $class();
            }
        }
    }

    private function configureContainer(ContainerConfigurator $container): void
    {
        $container->import('../config/packages/*.yaml');
        $container->import('../config/services.yaml');
    }

    private function configureRoutes(RoutingConfigurator $routes): void
    {
        $routes->import('../config/routes.yaml');
    }
}

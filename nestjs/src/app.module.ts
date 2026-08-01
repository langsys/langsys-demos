import { Module, type MiddlewareConsumer, type NestModule } from '@nestjs/common';
import { LangsysModule, LangsysLocaleMiddleware } from 'langsys-js-nestjs';
import { AppController } from './app.controller';
import { LOCALES, apiUrl, key, projectid } from './langsys.config';

@Module({
    imports: [
        LangsysModule.forRoot({
            projectid,
            key, // the shared demo key is read-only; your own write key enables discovery
            apiUrl,
            baseLocale: 'en-US',
            supportedLocales: Object.keys(LOCALES),
        }),
    ],
    controllers: [AppController],
})
export class AppModule implements NestModule {
    configure(consumer: MiddlewareConsumer) {
        consumer.apply(LangsysLocaleMiddleware).forRoutes('*');
    }
}

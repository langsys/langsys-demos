import { Controller, Get, Header, Query } from '@nestjs/common';
import { Locale, T, type ServerTFunction } from 'langsys-js-nestjs';
import { banner } from './langsys.config';
import { renderDemo } from './render';

@Controller()
export class AppController {
    @Get()
    @Header('Content-Type', 'text/html; charset=utf-8')
    home(@T() t: ServerTFunction, @Locale() locale: string, @Query('count') countRaw?: string): string {
        const count = Math.max(0, Math.min(99, Number.parseInt(countRaw ?? '3', 10) || 0));
        return renderDemo({ t, locale, count, banner, framework: 'NestJS', docsPath: 'learn/guides/node' });
    }
}

import 'reflect-metadata';
import { NestFactory } from '@nestjs/core';
import type { NestExpressApplication } from '@nestjs/platform-express';
import { join } from 'node:path';
import { AppModule } from './app.module';

async function bootstrap(): Promise<void> {
    const app = await NestFactory.create<NestExpressApplication>(AppModule);
    app.useStaticAssets(join(__dirname, '..', 'public'));
    const port = Number.parseInt(process.env.PORT ?? '3000', 10);
    await app.listen(port);
    console.log(`Langsys × NestJS demo → http://localhost:${port}`);
}

void bootstrap();

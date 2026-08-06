import { bootstrapApplication } from '@angular/platform-browser';
import { provideLangsys } from 'langsys-js-angular';
import { AppComponent } from './app.component';
import { langsysConfig } from './langsys';

// provideLangsys() registers the SDK and initializes it during bootstrap — the
// Angular-idiomatic equivalent of the other demos' `import './langsys'` init.
// (Global styles come from src/demo.css, wired in angular.json.)
bootstrapApplication(AppComponent, {
    providers: [provideLangsys(langsysConfig)],
}).catch((err) => console.error(err));

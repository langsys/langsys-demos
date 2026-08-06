import { Component } from '@angular/core';
import { TranslatePipe } from 'langsys-js-angular';

// t() — inline string, in a component (docs.langsys.dev/learn/sdk/angular).
@Component({
    selector: 'app-greeting',
    standalone: true,
    imports: [TranslatePipe],
    template: `<p>{{ 'Hello, {name}!' | t: 'Greetings' : { name: name } }}</p>`,
})
export class GreetingComponent {
    readonly name = 'Sarah';
}

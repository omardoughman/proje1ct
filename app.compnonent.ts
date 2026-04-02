import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'PiHub UI';

  message = 'Hello from Angular + PiHub';

  logs: string[] = [];

  addLog() {
    this.logs.push('Log at ' + new Date().toLocaleTimeString());
  }
}

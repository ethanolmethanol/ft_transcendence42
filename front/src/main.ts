import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/Pages/defaultPage/app.component';
import { RootComponent } from './app/Pages/mainPage/root.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
bootstrapApplication(RootComponent, appConfig)
  .catch((err) => console.error(err));

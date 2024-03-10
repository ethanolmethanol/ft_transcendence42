import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import {SignInPageComponent} from "./app/Pages/sign-in-page/sign-in-page.component"

bootstrapApplication(SignInPageComponent, appConfig)
  .catch((err) => console.error(err));

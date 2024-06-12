import { Routes } from '@angular/router';
import { SignUpPageComponent } from './pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';
import { HomePageComponent } from "./pages/home-page/home-page.component";
import { AuthGuard } from "./guards/auth.guard";
import { GuestGuard } from "./guards/guest.guard";
import { GamePageComponent } from "./pages/game-page/game-page.component";
import { MonitorPageComponent } from "./pages/monitor-page/monitor-page.component";
import { CreateOnlineGamePageComponent } from './pages/create-online-game-page/create-online-game-page.component';
import {OnlineGameSelectorPageComponent} from "./pages/online-game-selector-page/online-game-selector-page.component";

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomePageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'local', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'local' } },
  { path: 'local/:channel_id/:arena_id', component: GamePageComponent, pathMatch: 'prefix', canActivate: [AuthGuard], data: { gameType: 'local' } },
  { path: 'online', component: OnlineGameSelectorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online' } },
  { path: 'online/create/options', component: CreateOnlineGamePageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online' } },
  { path: 'online/create/waiting', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online', actionType: 'create'} },
  { path: 'online/join', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online' , actionType: 'join'} },
  { path: 'online/:channel_id/:arena_id', component: GamePageComponent, pathMatch: 'prefix', canActivate: [AuthGuard], data: { gameType: 'online' } },
  { path: 'sign-in', component: SignInPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: 'sign-up', component: SignUpPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full' },
  { path: '**', redirectTo: '/404' },
];

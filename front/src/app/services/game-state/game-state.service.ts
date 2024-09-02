import { Injectable } from '@angular/core';
import {BehaviorSubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class GameStateService {
  private _dataLoaded = new BehaviorSubject<boolean>(false);
  private _isWaiting = new BehaviorSubject<boolean>(true);
  private _isRemote = new BehaviorSubject<boolean>(true);
  private _isRematch = new BehaviorSubject<boolean>(true);
  private _channelID = new BehaviorSubject<string>('');
  private _isTournament = new BehaviorSubject<boolean>(false);
  private _activePlayers = new BehaviorSubject<string[]>([]);
  private _channelPlayers = new BehaviorSubject<string[]>([]);
  private _channelCapacity = new BehaviorSubject<number>(2);
  private _maxPlayers = new BehaviorSubject<number>(2);

  get dataLoaded$() { return this._dataLoaded.asObservable(); }
  get isWaiting$() { return this._isWaiting.asObservable(); }
  get isRemote$() { return this._isRemote.asObservable(); }
  get isRematch$() { return this._isRematch.asObservable(); }
  get channelID$() { return this._channelID.asObservable(); }
  get isTournament$() { return this._isTournament.asObservable(); }
  get activePlayers$() { return this._activePlayers.asObservable(); }
  get channelPlayers$() { return this._channelPlayers.asObservable(); }
  get channelCapacity$() { return this._channelCapacity.asObservable(); }
  get maxPlayers$() { return this._maxPlayers.asObservable(); }


  setDataLoaded(value: boolean) { this._dataLoaded.next(value); }
  setIsWaiting(value: boolean) { this._isWaiting.next(value); }
  setIsRemote(value: boolean) { this._isRemote.next(value); }
  setIsRematch(value: boolean) { this._isRematch.next(value); }
  setChannelID(value: string) { this._channelID.next(value); }
  setIsTournament(value: boolean) { this._isTournament.next(value); }
  setActivePlayers(value: string[]) { this._activePlayers.next(value); }
  setChannelPlayers(value: string[]) { this._channelPlayers.next(value); }
  setChannelCapacity(value: number) { this._channelCapacity.next(value); }
  setMaxPlayers(value: number) { this._maxPlayers.next(value); }

  restrictReset() {
    this.setDataLoaded(false);
    this.setIsWaiting(true);
  }

  reset() {
    this.restrictReset();
    this.setIsRemote(true);
    this.setIsRematch(true);
    this.setChannelID('');
    this.setIsTournament(false);
    this.setActivePlayers([]);
    this.setChannelPlayers([]);
    this.setChannelCapacity(2);
    this.setMaxPlayers(2);
  }
}

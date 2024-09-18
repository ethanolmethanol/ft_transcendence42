import { Injectable } from '@angular/core';
import {BehaviorSubject} from "rxjs";
import {TournamentMap} from "../../interfaces/tournament-map.interface";

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
  private _tournamentMap = new BehaviorSubject<TournamentMap>({rounds_map: {}, winner: null});
  private _activePlayers = new BehaviorSubject<string[]>([]);
  private _channelPlayers = new BehaviorSubject<string[]>([]);
  private _channelCapacity = new BehaviorSubject<number>(2);
  private _maxPlayers = new BehaviorSubject<number>(2);
  private _canGiveUp = new BehaviorSubject<boolean>(true);

  get dataLoaded$() { return this._dataLoaded.asObservable(); }
  get isWaiting$() { return this._isWaiting.asObservable(); }
  get isRemote$() { return this._isRemote.asObservable(); }
  get isRematch$() { return this._isRematch.asObservable(); }
  get channelID$() { return this._channelID.asObservable(); }
  get isTournament$() { return this._isTournament.asObservable(); }
  get tournamentMap$() { return this._tournamentMap.asObservable(); }
  get activePlayers$() { return this._activePlayers.asObservable(); }
  get channelPlayers$() { return this._channelPlayers.asObservable(); }
  get channelCapacity$() { return this._channelCapacity.asObservable(); }
  get maxPlayers$() { return this._maxPlayers.asObservable(); }
  get canGiveUp$() { return this._canGiveUp.asObservable(); }

  setDataLoaded(value: boolean) { this._dataLoaded.next(value); }
  setIsWaiting(value: boolean) { this._isWaiting.next(value); }
  setIsRemote(value: boolean) { this._isRemote.next(value); }
  setIsRematch(value: boolean) { this._isRematch.next(value); }
  setChannelID(value: string) { this._channelID.next(value); }
  setIsTournament(value: boolean) { this._isTournament.next(value); }
  setTournamentMap(value: TournamentMap) { this._tournamentMap.next(value); }
  setActivePlayers(value: string[]) { this._activePlayers.next(value); }
  setChannelPlayers(value: string[]) { this._channelPlayers.next(value); }
  setChannelCapacity(value: number) { this._channelCapacity.next(value); }
  setMaxPlayers(value: number) { this._maxPlayers.next(value); }
  setCanGiveUp(value: boolean) { this._canGiveUp.next(value); }

  restrictReset() {
    this.setDataLoaded(false);
    this.setIsWaiting(true);
    this.setIsRematch(true);
    this.setCanGiveUp(false);
  }

  reset() {
    this.restrictReset();
    this.setIsRemote(true);
    this.setChannelID('');
    this.setIsTournament(false);
    this.setTournamentMap({rounds_map: {}, winner: null});
    this.setActivePlayers([]);
    this.setChannelPlayers([]);
    this.setChannelCapacity(2);
    this.setMaxPlayers(2);
  }
}

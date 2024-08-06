import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CountGamesComponent } from './count-games.component';

describe('CountGamesComponent', () => {
  let component: CountGamesComponent;
  let fixture: ComponentFixture<CountGamesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CountGamesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CountGamesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

/*

RERO ILS
Copyright (C) 2019 RERO

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AggregationComponent } from './aggregation.component';

describe('AggregationComponent', () => {
  let component: AggregationComponent;
  let fixture: ComponentFixture<AggregationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AggregationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AggregationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
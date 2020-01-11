import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { MatPaginator, MatTableDataSource } from '@angular/material';
import { Observable, Subscription } from 'rxjs';
import { WebSocketService } from '../common/services/web-socket.service';
import { NotificationsService } from '../common/services/notifications.service';
import { SharedDataService } from '../common/services/shared-data.service';
import { environment } from '../../environments/environment';
import { constant } from '../../environments/constants';
import { Router } from '@angular/router';

@Component({
  selector: 'app-manage-grievance',
  templateUrl: './manage-grievance.component.html',
  styleUrls: ['./manage-grievance.component.scss']
})
export class ManageGrievanceComponent implements OnInit, OnDestroy {

  private subscription: Subscription = new Subscription();

  constructor(public webSocketService: WebSocketService,
    public notificationsService: NotificationsService,
    public sharedDataService: SharedDataService,
    public _router: Router) { }

  // tslint:disable-next-line: max-line-length
  grievanceDisplayedColumns: string[] = ['complainant_name', 'ministry_department', 'grievance_issue', 'complainant_city', 'complainant_mobile', 'complainant_email', 'icon'];
  grievanceDataSource: any;
  grievance_json: Array<object>;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {
    this.grievance_json = new Array<object>();
    this.getGrievance();
    this.paginator.pageIndex = +localStorage.getItem('grievance_pageIndex');
    this.paginator.pageSize = +localStorage.getItem('grievance_pageSize');
  }

  getGrievance() {
    this.webSocketService.createGrievanceRoom('grievance');
    this.webSocketService.getGrievance('grievance').subscribe(grievance => {
      this.grievance_json = grievance;
      this.grievanceDataSource = new MatTableDataSource(this.grievance_json);
      this.grievanceDataSource.paginator = this.paginator;
    },
      err => console.error('Observer got an error: ' + err),
      () => console.log('Observer got a complete notification'));
  }

  applyGrievanceFilter(filterValue: string) {
    this.grievanceDataSource.filter = filterValue.trim().toLowerCase();
  }

  getGrievancePaginatorData(event: any) {
    localStorage.setItem('grievance_pageIndex', event.pageIndex);
    localStorage.setItem('grievance_pageSize', event.pageSize);
  }

  openGrievanceChat(grievance_id: string) {
    this.sharedDataService.setSharedData('grievance_id', grievance_id, constant.MODULE_COMMON);
    const curr_grievance = this.grievance_json.filter(grievance => grievance['sender_id'] === grievance_id);
    this.sharedDataService.setSharedData('grievance_json', curr_grievance, constant.MODULE_COMMON);
    this._router.navigate(['/home/grievance-chat']);
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
    this.webSocketService.leaveGrievanceRoom('grievance');
  }

}

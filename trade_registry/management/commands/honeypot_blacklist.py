from django.core.management.base import BaseCommand
from trade_registry.models import BlacklistedIP


class Command(BaseCommand):
    help = "Manage honeypot IP blacklist"

    def add_arguments(self, parser):
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all blacklisted IPs',
        )
        parser.add_argument(
            '--add',
            type=str,
            help='Add an IP to blacklist',
        )
        parser.add_argument(
            '--remove',
            type=str,
            help='Remove an IP from blacklist',
        )
        parser.add_argument(
            '--reason',
            type=str,
            help='Reason for blacklisting (use with --add)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear entire blacklist',
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_blacklist()
        elif options['add']:
            self.add_ip(options['add'], options.get('reason', ''))
        elif options['remove']:
            self.remove_ip(options['remove'])
        elif options['clear']:
            self.clear_blacklist()
        else:
            self.stdout.write(self.style.WARNING('Use --list, --add, --remove, or --clear'))

    def list_blacklist(self):
        ips = BlacklistedIP.objects.all()
        if not ips.exists():
            self.stdout.write(self.style.SUCCESS('Blacklist is empty'))
            return

        self.stdout.write(self.style.SUCCESS('\n=== Blacklisted IPs ===\n'))
        for entry in ips:
            self.stdout.write(
                f"IP: {entry.ip_address:15} | Attempts: {entry.attempt_count:2} | "
                f"Last: {entry.last_attempt.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Reason: {entry.reason}"
            )
        self.stdout.write(self.style.SUCCESS(f'\nTotal: {ips.count()} IPs\n'))

    def add_ip(self, ip, reason=''):
        try:
            obj, created = BlacklistedIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': reason}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added {ip} to blacklist'))
            else:
                self.stdout.write(self.style.WARNING(f'{ip} already in blacklist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

    def remove_ip(self, ip):
        try:
            BlacklistedIP.objects.get(ip_address=ip).delete()
            self.stdout.write(self.style.SUCCESS(f'Removed {ip} from blacklist'))
        except BlacklistedIP.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'{ip} not in blacklist'))

    def clear_blacklist(self):
        count = BlacklistedIP.objects.count()
        BlacklistedIP.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Cleared {count} IPs from blacklist'))

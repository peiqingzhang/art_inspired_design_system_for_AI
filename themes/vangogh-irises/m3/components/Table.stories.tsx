import type { Meta, StoryObj } from '@storybook/react';
import Table from './Table';

const meta  : Meta<typeof Table> = {
  title: 'Components/Table',
  component: Table,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Table>;

export const Default: Story = { args={{ columns: [{ key: 'name', header: 'Name' }], data: [{ name: 'Row 1' }] }} };
export const Striped: Story = { args={{ columns: [{ key: 'name', header: 'Name' }], data: [{ name: 'Row 1' }, { name: 'Row 2' }], striped: true }} };
